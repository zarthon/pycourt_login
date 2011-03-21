from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
'''Import forms and User profile'''
from pycourt_login import forms as myforms
from django.core.mail import *
import datetime
from pycourt_login.dataplus import *
from django.core.mail import EmailMultiAlternatives
from pycourt_login.models import PasswordCHangeRequest 
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
                return HttpResponseRedirect('/home/')
            else:
                return HttpResponse('fail')
        else:
            return render_to_response('login.html',{'form':forms,'login':True,'data':request.POST},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def logout(request): 
    auth_logout(request)
    return HttpResponseRedirect('/login/')

def register(request):
    if not request.user.is_authenticated():
        form = myforms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username = request.POST["username"],password=request.POST["password1"])
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
        print request.REQUEST.keys()
        print request.REQUEST.values()
        form = myforms.ResetForm(request.POST)
        if form.is_valid() and change_req:
            user = change_req.account
            print dictGetval(request.REQUEST,"password2")
            user.set_password(dictGetval(request.REQUEST,"password2"))
            user.save()
            change_req.delete()
            return HttpResponseRedirect('/')
        else:
            print form
            return render_to_response("resetpassword.html",{'form':form,'reset':True,'data':request.POST},context_instance=RequestContext(request))
 

def home(request):
    home = True
    return render_to_response('home.html',locals(),context_instance=RequestContext(request))
        
