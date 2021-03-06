from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core import serializers
from django.contrib.auth.models import Group
from pycourt_login.models import *
from django.db.models import Q
'''Import forms and User profile'''
from pycourt_login import forms as myforms
from django.core.mail import *
import datetime
from time import mktime
from pycourt_login.dataplus import *
from django.core.mail import EmailMultiAlternatives
from pycourt_login.models import PasswordCHangeRequest, Dishes
import threading

counterid_list = ['counter1','counter2','counter3']
#Global Timer Object
TIMER=None

#Change status to False for all counters (in case its true due to server closing unexpectedly)
loginstatus_all = LoginStatus.objects.filter(status=True)
for obj in loginstatus_all:
	obj.status = False
	obj.save()

def disableCounter(user):
	print "Inside disable counter"
	print "User==>"+str(user.username)
	counter_obj = LoginStatus.objects.get(counterid = user)
	counter_obj.status = False
	counter_obj.save()

def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')
	else:
		return HttpResponseRedirect('/home')

def login(request):
	if not request.user.is_authenticated():
		forms = myforms.LoginForm(request.POST)
		if forms.is_valid():
			user = authenticate(username=request.POST["username"],password=request.POST["password"])
			if user is not None:
				auth_login(request,user)
				request.session.set_expiry(3000)
				request.session['member_id'] = user.id
				if user.username in counterid_list:
					status_obj = LoginStatus.objects.get(counterid = user)
					status_obj.status = True
					status_obj.save()
				return HttpResponseRedirect('/home/')
			else:
				return render_to_response('wrong.html',{},context_instance=RequestContext(request))
		else:
			return render_to_response('login.html',{'form':forms,'login':True,'data':request.POST},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def logout(request):
    if request.user.username in counterid_list:
	    status_obj = LoginStatus.objects.get(counterid = request.user)
	    status_obj.status = False
	    status_obj.save()
    auth_logout(request)
    return render_to_response('logout.html',{},context_instance=RequestContext(request))

def register(request):
	if not request.user.is_authenticated():
		form = myforms.RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(username = request.POST["username"],password=request.POST["password1"])
			if user.username == 'counter1' or user.username == 'counter2' or user.username == 'counter3':
				counter = True
				student = False
				userprof = UserProfile(user = user,is_counter = counter,is_student=student)
				userprof.save()
				account = CounterAccount(account = user,balance =0)
				account.save()

			else:
				counter = False
				student = True
				userprof = UserProfile(user = user,is_counter = counter,is_student=student)
				userprof.save()
				account = BalanceAccount(account=user, counter1_balance=0,counter2_balance=0,counter3_balance=0)
				account.save()
			auth_login(request,user)
			return HttpResponseRedirect('/')
		else:
			return render_to_response("signup.html",{'signup_form':form,'signup':True,'data':request.POST},context_instance=RequestContext(request))


def forgot_password(request):
    if not request.user.is_authenticated():
        form = myforms.ForgotForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = request.POST["username"])
            password_change_req = models.PasswordCHangeRequest()
            password_change_req.account = user
            uniqueId = getUniqueId()
            password_change_req.req_random_key = uniqueId
            password_change_req.created_at = datetime.datetime.utcnow()
            password_change_req.save()

            mail_subject = 'Reset your Pycourt password'
            mail_body = '<p>Hello,</p>'
            mail_body += '<p>You received this email because a Password Reset was requested for your Pycourt account. <br />'
            mail_body += 'Just click the link <a href="http://'+str(request.get_host())+'/resetpass/?passwordChangeKey='+ uniqueId + '"><strong>Reset My Password</strong></a> to change your password.</p>'
            mail_body += '<p>If you did not request it, you can safely ignore this mail.</p>'
            mail_body += '<p>Regards,<br />from Pycourt</p>'		   
            msg = EmailMessage(mail_subject,mail_body,"200801066@daiict.ac.in",[str(user.email)])
            msg.content_subtype = "html"
#			msg.send()
#			return HttpResponse(str(user.email))
#			user.email_user(mail_subject,mail_body,"200801066@daiict.ac.in")
            return HttpResponse(mail_body)
        else:
            return render_to_response('forget.html',{'form':form,'forget':True,'data':request.POST},context_instance=RequestContext(request))
            #return HttpResponseRedirect('/login')


def resetpassword(request):
	passkey = dictGetval(request.REQUEST,'passwordChangeKey')
	change_req = returnIfExists(PasswordCHangeRequest.objects.filter(req_random_key=passkey,created_at__gte=(datetime.datetime.utcnow()-datetime.timedelta(2))))
	if request.method == 'GET':
		return render_to_response("resetpassword.html",{'passwordChangeKey':dictGetval(request.REQUEST,"passwordChangeKey"),'reset':True,'data':request.POST},context_instance=RequestContext(request))
	elif request.method == 'POST':
		form = myforms.ResetForm(request.POST)
		if form.is_valid() and change_req:
			user = change_req.account
			user.set_password(dictGetval(request.REQUEST,"password2"))
			user.save()
			change_req.delete()
			return HttpResponseRedirect('/')
		else:
			return render_to_response("resetpassword.html",{'form':form,'reset':True,'data':request.POST},context_instance=RequestContext(request))
 

def home(request):
	userprof = UserProfile.objects.all()
	userprofile=None

	for u in userprof:
		if u.user.username == request.user.username:
			userprofile = u
		
	if request.user.is_authenticated():
		if userprofile is None:
			return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'User is not Counter and Student'},context_instance = RequestContext(request))

		home = True
		dishes = Dishes.objects.all()
	
		#print userprofile.user.username

		counter_1 = dishes.filter(counter1 = True)
		counter_2 = dishes.filter(counter2 = True)
		counter_3 = dishes.filter(counter3 = True)
		order_list = list()
		if userprofile.is_counter == True:
			user  = userprofile.user
			counter_account = CounterAccount.objects.get(account = request.user)
			if user.username == 'counter1':
				count = 0
			elif user.username == 'counter2':
				count = 1
			elif user.username == 'counter3':
				count = 2
			else:
				return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'Counter\'s User id Doesnot exist in Database'},context_instance = RequestContext(request))

			counter = [counter_1,counter_2,counter_3][count]
			orders = Orders.objects.filter(counterid=user.username,delivered=False)
			if orders is None:
				return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'No Current Orders in Database'},context_instance = RequestContext(request))
			else:
				for o in orders:
					t = o.order_id
					r = t.split('count')
					dish = Dishes.objects.get(id=r[0])
					print dish.dish_name

		elif userprofile.is_student == True:
				student_account = BalanceAccount.objects.get(account=request.user)
				counter1_obj = User.objects.get(username = 'counter1')
				counter2_obj = User.objects.get(username = 'counter2')
				counter3_obj = User.objects.get(username = 'counter3')
				counter1_stat = LoginStatus.objects.get(counterid=counter1_obj)
				counter2_stat = LoginStatus.objects.get(counterid=counter2_obj)
				counter3_stat = LoginStatus.objects.get(counterid=counter3_obj)
				print student_account.counter1_balance
		return render_to_response('home.html',locals(),context_instance=RequestContext(request))
	else:
		return render_to_response('home.html',locals(),context_instance=RequestContext(request))

@login_required
def profile(request):
	user = request.user
	if user is None:
		return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'LOL'},context_instance = RequestContext(request))
	else:
		return render_to_response('profile.html',locals(),context_instance=RequestContext(request))

@login_required
def setting(request):
	user = request.user
	forms = myforms.SettingForm(instance=request.user)
	print "OUTSIDE POST"
	print forms
	if request.method == 'POST':
		print "INSIDE POST"
		print request.POST
		forms = myforms.SettingForm(request.POST,instance=request.user)
		print "asdsda"
		print forms
		if forms.is_valid():
			forms.save()
			return HttpResponseRedirect('/home/?thanks=profilechange')
		else:
			request.user = user
	  #	  return render_to_response('setting.html',{'signup_form':forms,'data':request.POST},context_instance=RequestContext(request))
	return render_to_response('setting.html',{'signup_form':forms,'data':request.POST,'user':user},context_instance=RequestContext(request))

@login_required
def order(request):
	# 1count2%3 -> Dishes.id=1;Counter_no=2;Quantity=3

	user = request.user
	orders = list()
	account2_list = list()
	count =0
	if(request.method == 'POST'):
		orderno = request.POST["order"]
		orderlist = orderno.split(',')

		#Student Account is account1
		account1 = BalanceAccount.objects.get(account=user)
		transid = request.user.username+str(mktime(datetime.datetime.now().timetuple()))[:-2]
		for i in range(0,len(orderlist)-1):
			order_param = orderlist[i].split("%")
			quantity = order_param[1]
			orderid = order_param[0].split("count")
			if orderid[1] == '1':
				counter = 'counter1'
			elif orderid[1]=='2':
				counter = 'counter2'
			else:
				counter = 'counter3'

			counter_obj = User.objects.get(username = counter)
			counter_alive = LoginStatus.objects.get(counterid = counter_obj)

			dish = Dishes.objects.get(id = int(orderid[0]))
			
			counterac = User.objects.get(username=counter)
			account2 = CounterAccount.objects.get(account=counterac)

			if not counter_alive.status:
					return render_to_response("ShowMessage.html",{'msg_html':'Counter 1 is Closed','msg_heading':'Sorry'},context_instance = RequestContext(request))
			
			if orderid[1] == '1':
				if not dish.counter1:
					return render_to_response("ShowMessage.html",{'msg_html':'Dish'+dish.dish_name+' is not currently available at counter 1','msg_heading':'Dish Unavailable at the moment'},context_instance = RequestContext(request))
				
				if account1.counter1_balance >= int(quantity)*int(dish.dish_price):
					account1.counter1_balance = account1.counter1_balance - int(quantity)*int(dish.dish_price)
					account2.balance = account2.balance + int(quantity)*int(dish.dish_price)
					counter = 'counter1'
				else:
					return render_to_response("ShowMessage.html",{'msg_html':'Insufficient Balance in Counter 1. Order is Discarded. Please Recharge Your account','msg_heading':'Insufficient Balance'},context_instance = RequestContext(request))

			elif orderid[1]=='2':
				if not dish.counter2:
					return render_to_response("ShowMessage.html",{'msg_html':'Dish'+dish.dish_name+' is not currently available at counter 2','msg_heading':'Dish Unavailable at the moment'},context_instance = RequestContext(request))


				if account1.counter2_balance >= int(quantity)*int(dish.dish_price):
					account1.counter2_balance = account1.counter2_balance - int(quantity)*int(dish.dish_price)
					account2.balance = account2.balance + int(quantity)*int(dish.dish_price)
					counter = 'counter2'
				else:
					return render_to_response("ShowMessage.html",{'msg_html':'Insufficient Balance in Counter 2. Order is Discarded. Please Recharge your Account','msg_heading':'Insufficient Balance'},context_instance = RequestContext(request))
			else:
				if not dish.counter3:
					return render_to_response("ShowMessage.html",{'msg_html':'Dish'+dish.dish_name+' is not currently available at counter 3','msg_heading':'Dish Unavailable at the moment'},context_instance = RequestContext(request))


				if account1.counter3_balance >= int(quantity)*int(dish.dish_price):
					account1.counter3_balance = account1.counter3_balance - int(quantity)*int(dish.dish_price)
					account2.balance = account2.balance + int(quantity)*int(dish.dish_price)
					counter = 'counter3'
				else:
					return render_to_response("ShowMessage.html",{'msg_html':'Insufficient Balance in Counter 3. Order is Discarded. Please Recharge your Account','msg_heading':'Insufficient Balance'},context_instance = RequestContext(request))

			order = Orders(order_id=orderlist[i],student_id=user,status=0,counterid=counter,datetime=datetime.datetime.now(),dish=dish,quantity=int(quantity),transaction_id=transid,delivered=False)

			orders.append(order)
			account2_list.append(account2)
			count +=1
		
		if count == len(orderlist)-1:
			for i in range(0,len(orders)):
				orders[i].save()
				account2_list[i].save()
		account1.save()
		order.save()
		return HttpResponseRedirect('/home/?thanks=orderdone&id='+transid)


@login_required
def history(request):
   userprof = UserProfile.objects.get(user= request.user) 
   if userprof.is_student:
	   	past_orders = Orders.objects.filter(student_id = request.user)
	   	sum = 0
		for order in past_orders:
			sum += int(order.dish.dish_price)*int(order.quantity)

	   	return render_to_response("accountsummary.html",locals(),context_instance=RequestContext(request))
   elif userprof.is_counter:
   		past_orders = Orders.objects.filter(counterid = request.user.username)
		sum = 0
		for order in past_orders:
			sum += int(order.dish.dish_price)*int(order.quantity)
		return render_to_response("accountsummary.html",locals(),context_instance=RequestContext(request))
   else:
	    return render_to_response("ShowMessage.html",{'msg_heading':'Trying to Hack this site!','msg_html':'UserProfile Does Not Exist'},contex_instance=RequestContext(request))

@login_required
def add_dish(request):
	userprof = UserProfile.objects.get(user=request.user)
	user = request.user
	if userprof.is_counter:
		if request.method == 'POST':
			form = myforms.AddDishForm(request.POST)
			if form.is_valid():
				dishname = request.POST["dishname"]
				dishprice = request.POST["dishprice"]
				if user.username == "counter1":
					counter1=True
					counter2 = False
					counter3 = False
				elif user.username == "counter2":
					counter2=True
					counter1 = False
					counter3 = False
				elif user.username == "counter3":
					counter1 = False
					counter2 = False
					counter3 = True
				else:
					counter1 = False
					counter2 = False
					counter3 = False
				dish = Dishes(dish_name = dishname, dish_price=int(dishprice),counter1 = counter1, counter2 = counter2, counter3 = counter3)
				print dish.dish_name, dish.dish_price
				dish.save()
				return HttpResponseRedirect("/home/")
			else:
				print form
				return render_to_response("adish.html",{'form':form,'data':request.POST},context_instance=RequestContext(request))
		else:
			form = myforms.AddDishForm()
			print form
			return render_to_response("adish.html",{'form':form},context_instance=RequestContext(request))
	else:
		return render_to_response("ShowMessage.html",{'msg_heading':'UnAuthorized Access','msg_html':'Only Counter Owners are authorized to add dishes not Students....:P'},context_instance=RequestContext(request))

def mostRecentTransaction(request):
	global TIMER
	cnt_user = request.user.username
	if TIMER is not None:
		TIMER.cancel()
	TIMER = threading.Timer(5.0,disableCounter,[request.user]) 
	TIMER.start()
	counter_obj = LoginStatus.objects.get(counterid = request.user)
	counter_obj.status = True
	counter_obj.save()

	if request.GET['id'] == u'0':
		order = Orders.objects.filter(counterid = cnt_user,delivered=False)
		if len(order) == 0:
			return HttpResponse("")
		else:
			print "we have orders"
			return HttpResponse('<p style="background-color: #E4F2E4">Food List outdated, please refresh</p>')
	else:
		transactid_lastdisplayed = request.GET['id'][9:]
		cnt_orders = Orders.objects.filter(counterid=cnt_user,delivered=False)
		latestid = cnt_orders.latest('id').transaction_id[9:]
		#latestid = Orders.objects.latest('counterid').transaction_id[9:]
		#print transactid_lastdisplayed 
		if latestid > transactid_lastdisplayed:
			return HttpResponse('<p style="background-color: #E4F2E4" >Food List outdated, please refresh</p>')
		else:
			return HttpResponse('')

@login_required
def changeStatus(request):
	if request.method == 'GET':
		orderpid = request.GET["id"]
		print "Order PK id --> "+orderpid
		userprof = UserProfile.objects.get(user= request.user)
		if userprof.is_counter:
			currentOrder = Orders.objects.get(id=int(orderpid))
			print currentOrder.status
			if currentOrder.status < 2:
				currentOrder.status=currentOrder.status+1
			elif currentOrder.status == 2:
				currentOrder.delivered=True
			else:
				return render_to_response("ShowMessage.html",{'msg_heading':'UnAuthorized Access','msg_html':'Something went wrong..'},context_instance=RequestContext(request))
			currentOrder.save()
			return HttpResponse("success")
		else:
			return HttpResponse("Dont try to hack the site")

def recharge_acc(request):
	userprof = UserProfile.objects.get(user =request.user)
	if userprof.is_counter:
		cnt_user = request.user
		if request.method == "POST":
			form = myforms.RechargeForm(request.POST)
			if form.is_valid():
				print request.POST
				username = request.POST["username"]
				password = request.POST["password"]
				amount = request.POST["amount"]
				print amount
				stu_user = authenticate(username=request.POST["username"],password=request.POST["password"])
				if stu_user is not None:
					account = BalanceAccount.objects.get(account = stu_user)
					print "asdasda"
					print account
					if cnt_user.username == "counter1":
						account.counter1_balance +=int(amount)
						print account.counter1_balance
					elif cnt_user.username == "counter2":
						account.counter2_balance += int(amount)
						print account.counter2_balance
					elif cnt_user.username == "counter3":
						account.counter3_balance += int(amount)
						print account.counter3_balance
					else:
						return render_to_response("ShowMessage.html",{'msg_heading':'UnAuthorized Access','msg_html':'Counter Owner is not Registered....:P'},context_instance=RequestContext(request))
	
					account.save()
					return HttpResponseRedirect("/home/") 
				else:
					pass_inc = True
					return render_to_response( "recharge.html", {'form':form,'pass_inc':pass_inc,'data':request.POST}, context_instance=RequestContext(request) )
			else:
				print form
				return render_to_response( "recharge.html", {'form':form,'data':request.POST}, context_instance=RequestContext(request) )
		else:
			form = myforms.RechargeForm()
			print form
			return render_to_response("recharge.html",{'form':form},context_instance=RequestContext(request))
	else:
		return render_to_response("ShowMessage.html",{'msg_heading':'UnAuthorized Access','msg_html':'Only Counter Owners are authorized to Recharge Accounts....:P'},context_instance=RequestContext(request))

@login_required
def changeAvailability(request):
	if request.method == 'GET':
		orderpid = request.GET["id"]
		userprof = UserProfile.objects.get(user= request.user)
		if userprof.is_counter:
			cnt_user = request.user
			dish_object = Dishes.objects.get(id=orderpid)
			if cnt_user.username == "counter1":
				dish_object.counter1 = not dish_object.counter1
				dish_object.save()
				return HttpResponse("success")
			if cnt_user.username == "counter2":
				dish_object.counter2 = not dish_object.counter2
				dish_object.save()
				return HttpResponse("success")
			if cnt_user.username == "counter3":
				dish_object.counter3 = not dish_object.counter3
				dish_object.save()
				return HttpResponse("success")

def pendingOrders(request):
		userprof = UserProfile.objects.get(user= request.user)
		if userprof.is_student:
			student_account = request.user
			dish = Dishes.objects.all()
			#Getting all pending orders
			order_all_pending = Orders.objects.filter(student_id = student_account,delivered = False)
			pending_orders = Orders.objects.filter(~Q(status = 2),delivered = False)
			for order in order_all_pending:
				#Hack to change QuerySet to pass as JSON 
				order.quantity = pending_orders.filter(id__lt = order.id,counterid= order.counterid).count() + 1
			
			#Returning JSON response to the objects obtained in above statement
			return HttpResponse(serializers.serialize('json',order_all_pending,use_natural_keys=True),mimetype='application/json')
		else:
			return HttpResponse("Something went wrong")

def help(request):
	return render_to_response("help.html")
