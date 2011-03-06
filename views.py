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

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/logout')
    else:
        return HttpResponseRedirect('/login')

def login(request):
    if not request.user.is_authenticated():
        forms = myforms.LoginForm(request.POST)
        if forms.is_valid():
            user = authenticate(username=request.POST["username"],password=request.POST["password"])
            #user.groups.add('temp')
            if user is not None:
                auth_login(request,user)
                print user.get_all_permissions()
                return HttpResponseRedirect('/logout/')
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
            mail_body += '<p>You received this email because a Password Reset was requested for your Socialray account. <br />'
            mail_body += 'Just click the link <a href="http://www.abcd.com/resetpassword.htm?' + \
                'passwordChangeKey=' + uniqueId + '"><strong>Reset My Password</strong></a> to change your password.</p>'
            mail_body += '<p>If you did not request it, you can safely ignore this mail.</p>'
            mail_body += '<p>Regards,<br />from Pycourt</p>'           
            msg = EmailMessage(mail_subject,mail_body,"200801066@daiict.ac.in",[str(user.email)])
            msg.content_subtype = "html"
            msg.send()
#            user.email_user(mail_subject,mail_body,"200801066@daiict.ac.in")
            return HttpResponse("Your email address is %s"%user.email)
        else:
            return render_to_response('forget.html',{'form':form,'forget':True,'data':request.POST},context_instance=RequestContext(request))
            #return HttpResponseRedirect('/login')
[TO DO]
def resetpassword(request):
    passkey = dictGetval(request.REQUEST,'passwordChangeKey','')
    change_req = returnIfExists(models.PasswordChangeRequest.objects.filter(req_random_key=passkey,created_at_gte=(datetime.datetime.utcnow()-datetime.delta(1))))

    if not change_req:
        return render_to_response('showmessage.html',{'msg_heading':'Password Reset'})
    if request.method == 'GET':
        pass
