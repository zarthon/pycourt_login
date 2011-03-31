from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.models import Group
from pycourt_login.models import *
'''Import forms and User profile'''
from pycourt_login import forms as myforms
from django.core.mail import *
import datetime
from time import mktime
from pycourt_login.dataplus import *
from django.core.mail import EmailMultiAlternatives
from pycourt_login.models import PasswordCHangeRequest, Dishes

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
            #user.groups.add('temp')
            if user is not None:
                auth_login(request,user)
                #request.session.set_expiry(300)
                #print request.session.get_expiry_date()
                request.session['member_id'] = user.id
                temp = UserProfile.objects.get(user = user)
                print temp.is_counter , temp.is_student
                return HttpResponseRedirect('/home/')
            else:
                return render_to_response('wrong.html',{},context_instance=RequestContext(request))
        else:
            return render_to_response('login.html',{'form':forms,'login':True,'data':request.POST},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def logout(request): 
    auth_logout(request)
    return render_to_response('logout.html',{},context_instance=RequestContext(request))

def register(request):
    if not request.user.is_authenticated():
        form = myforms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username = request.POST["username"],password=request.POST["password1"])
            if user.username == '123456789' or user.username == '123456788' or user.username == '123456777':
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
            mail_body += 'Just click the link <a href="http://127.0.0.1:8000/resetpass/?passwordChangeKey='+ uniqueId + '"><strong>Reset My Password</strong></a> to change your password.</p>'
            mail_body += '<p>If you did not request it, you can safely ignore this mail.</p>'
            mail_body += '<p>Regards,<br />from Pycourt</p>'           
            msg = EmailMessage(mail_subject,mail_body,"200801066@daiict.ac.in",[str(user.email)])
            msg.content_subtype = "html"
#            msg.send()
#            return HttpResponse(str(user.email))
#            user.email_user(mail_subject,mail_body,"200801066@daiict.ac.in")
            return HttpResponse(mail_body)
        else:
            return render_to_response('forget.html',{'form':form,'forget':True,'data':request.POST},context_instance=RequestContext(request))
            #return HttpResponseRedirect('/login')


def resetpassword(request):
    passkey = dictGetval(request.REQUEST,'passwordChangeKey')
    change_req = returnIfExists(PasswordCHangeRequest.objects.filter(req_random_key=passkey,created_at__gte=(datetime.datetime.utcnow()-datetime.timedelta(1))))
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
            if user.username == '123456789':
                count = 0
            elif user.username == '123456788':
                count = 1
            elif user.username == '123456777':
                count = 2
            else:
                return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'Counter\'s User id Doesnot exist in Database'},context_instance = RequestContext(request))

            counter = [counter_1,counter_2,counter_3][count]
            orders = Ordersss.objects.filter(counterid=int(user.username),status=False)
            if orders is None:
                return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'No Current Orders in                    Database'},context_instance = RequestContext(request))
            else:
                for o in orders:
                    t = o.order_id
                    r = t.split('count')
                    dish = Dishes.objects.get(id=r[0])
                    print dish.dish_name

        elif userprofile.is_student == True:
                student_account = BalanceAccount.objects.get(account=request.user)
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
            return HttpResponseRedirect('/home/')
        else:
            request.user = user
      #      return render_to_response('setting.html',{'signup_form':forms,'data':request.POST},context_instance=RequestContext(request))
    return render_to_response('setting.html',{'signup_form':forms,'data':request.POST,'user':user},context_instance=RequestContext(request))

@login_required
def order(request):
    user = request.user
    orders = list()
    account2_list = list()
    count =0
    if(request.method == 'POST'):
        orderno = request.POST["order"]
        orderlist = orderno.split(',')

        #Student Account is account1
        account1 = BalanceAccount.objects.get(account=user)
        str(datetime.datetime.now().timetuple())
        transid = request.user.username+str(mktime(datetime.datetime.now().timetuple()))[:-2]
        print transid
        for i in range(0,len(orderlist)-1):
            order_param = orderlist[i].split("%")
            quantity = order_param[1]
            orderid = order_param[0].split("count")
            if orderid[1] == '1':
                counter = '123456789'
            elif orderid[1]=='2':
                counter = '123456788'
            else:
                counter = '123456777'
            print counter
        
            dish = Dishes.objects.get(id = int(orderid[0]))

            counterac = User.objects.get(username=counter)
            account2 = CounterAccount.objects.get(account=counterac)

            if orderid[1] == '1':
                print account1.counter1_balance, int(quantity)*int(dish.dish_price)
                if account1.counter1_balance >= int(quantity)*int(dish.dish_price):
                    account1.counter1_balance = account1.counter1_balance - int(quantity)*int(dish.dish_price)
                    account2.balance = account2.balance + int(quantity)*int(dish.dish_price)
                    counter = '123456789'
                else:
                    return render_to_response("ShowMessage.html",{'msg_html':'Insufficient Balance in Counter 1. Order                        is Discarded. Place new Order','msg_heading':'Insufficient Balance'},context_instance = RequestContext(request))

            elif orderid[1]=='2':
                if account1.counter2_balance >= int(quantity)*int(dish.dish_price):
                    account1.counter2_balance = account1.counter2_balance - int(quantity)*int(dish.dish_price)
                    account2.balance = account2.balance + int(quantity)*int(dish.dish_price)
                    counter = '123456788'
                else:
                    return render_to_response("ShowMessage.html",{'msg_html':'Insufficient Balance in Counter 2. Order                        is Discarded. Place new Order','msg_heading':'Insufficient Balance'},context_instance = RequestContext(request))
            else:
                if account1.counter3_balance >= int(quantity)*int(dish.dish_price):
                    account1.counter3_balance = account1.counter3_balance - int(quantity)*int(dish.dish_price)
                    account2.balance = account2.balance + int(quantity)*int(dish.dish_price)
                    counter = '123456777'
                else:
                    return render_to_response("ShowMessage.html",{'msg_html':'Insufficient Balance in Counter 3. Order                        is Discarded. Place new Order','msg_heading':'Insufficient Balance'},context_instance = RequestContext(request))

            order = Ordersss(order_id=orderlist[i],student_id=user,status=False,counterid=int(counter),datetime=datetime.datetime.now(),dish=dish,quantity=int(quantity),transaction_id=transid)

            orders.append(order)
            account2_list.append(account2)
            count +=1
        
        if count == len(orderlist)-1:
            for i in range(0,len(orders)):
                orders[i].save()
                account2_list[i].save()
        account1.save()
        order.save()
        return HttpResponseRedirect('/?thanks')


@login_required
def history(request):
   userprof = UserProfile.objects.get(user= request.user) 
   print userprof
   if userprof.is_student:
       past_orders = Ordersss.objects.filter(student_id = request.user)
       return render_to_response("accountsummary.html",locals(),context_instance=RequestContext(request))
   elif userprof.is_counter:
       pass
   else:
       return render_to_response("ShowMessage.html",{'msg_heading':'Trying to Hack this site!','msg_html':'UserProfile Does Not Exist'},contex_instance=RequestContext(request))
   return HttpResponse("hello")

@login_required
def add_dish(request):
    userprof = UserProfile.objects.get(user=request.user)
    user = request.user
    if userprof.is_counter:
        if request.method == 'POST':
            print "sdfasasdf"
            form = myforms.AddDishForm(request.POST)
            print request.POST
            if form.is_valid():
                print request.POST
                dishname = request.POST["dishname"]
                dishprice = request.POST["dishprice"]
                if user.username == "123456789":
                    counter1=True
                    counter2 = False
                    counter3 = False
                elif user.username == "123456788":
                    counter2=True
                    counter1 = False
                    counter3 = False
                elif user.username == "123456777":
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
	transactid_atdocument = request.GET['id'][9:]
	latestid = Ordersss.objects.latest('transaction_id').transaction_id[9:]
	print latestid, transactid_atdocument
	if latestid > transactid_atdocument:
		return HttpResponse('<p style="color:red">Food List outdated, please refresh</p>')
	else:
		return HttpResponse("")

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
                    if cnt_user.username == "123456789":
                        account.counter1_balance +=int(amount)
                        print account.counter1_balance
                    elif cnt_user.username == "123456788":
                        account.counter2_balance += int(amount)
                        print account.counter2_balance
                    elif cnt_user.username == "123456777":
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

