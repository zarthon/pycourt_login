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
                request.session.set_expiry(300)
                print request.session.get_expiry_date()
                request.session['member_id'] = user.id
                temp = UserProfile.objects.get(user = user)
                print temp.is_counter , temp.is_student
                return HttpResponseRedirect('/home/')
            else:
                return HttpResponse('fail')
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

            else:
                counter = False
                student = True
                userprof = UserProfile(user = user,is_counter = counter,is_student=student)
                userprof.save()
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
    home = True
    dishes = Dishes.objects.all()
    userprof = UserProfile.objects.all()
    userprofile=None
    for u in userprof:
        if u.user.username == request.user.username:
            userprofile = u

    #print userprofile.user.username
    counter_1 = dishes.filter(counter1 = True)
    counter_2 = dishes.filter(counter2 = True)
    counter_3 = dishes.filter(counter3 = True)

    return render_to_response('home.html',locals(),context_instance=RequestContext(request))

@login_required
def profile(request):
    user = request.user
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
    if(request.method == 'POST'):
        print request.POST
    orderno = request.POST["order"]
    orderlist = orderno.split(',')
    for i in range(0,len(orderlist)-1):
        orderid = orderlist[i].split("count")
        if orderid[1] == '1':
            counter = '123456789'
        elif orderid[1]=='2':
            counter = '123456788'
        else:
            counter = '123456777'
        print counter
    
        counterac = User.objects.get(username=counter)
        dish = Dishes.objects.get(dish_id = int(orderid[0]))
        account1 = BalanceAccount.objects.get(account=user)
        account2 = CounterAccount.objects.get(account=counterac)
        order = Orders(order_id=orderlist[i],student_id=user,status=False,counterid=int(counter))
        orders.append(order)

        if orderid[1] == '1' and account1.counter1_balance >= dish.dish_price:
            account1.counter1_balance = account1.counter1_balance -dish.dish_price
            account2.balance = account2.balance + dish.dish_price

        elif orderid[1]=='2'and account1.counter2_balance >= dish.dish_price:
            account1.counter1_balance = account1.counter1_balance -dish.dish_price
            account2.balance = account2.balance + dish.dish_price

            counter = '123456788'
        else:
            if account1.counter3_balance >= dish.dish_price:
                account1.counter3_balance = account1.counter3_balance -dish.dish_price
                account2.balance = account2.balance + dish.dish_price
            counter = '123456777'
        
        print account1.counter1_balance
        print order.order_id, order.student_id,order.status,order.date 
        account1.save()
        account2.save()
        order.save()
    return HttpResponse(str(order.student_id.username)+'////'+str(order.order_id)+'////'+str(order.counterid))
    



