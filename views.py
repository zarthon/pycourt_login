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
            print user
            if user is not None:
                auth_login(request,user)
                return HttpResponseRedirect('/logout/')
            else:
                return HttpResponse('fail')
        else:
            form = myforms.LoginForm()      
            return render_to_response('login.html',{'form':form},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def logout(request): 
    auth_logout(request)
    return HttpResponseRedirect('/login/')

def register(request):
    print "INSIDE Register"
    if not request.user.is_authenticated():
        form = myforms.RegisterForm(request.POST)
        print "Inside 2"
        if form.is_valid():
            print "Inside 3"
            form.save()
            user = authenticate(username = request.POST["username"],password=request.POST["password1"])
            auth_login(request,user)
            return HttpResponseRedirect('/')
        else:
            print form.errors
            return render_to_response("signup.html",{'signup_form':form,'signup':True,'data':request.POST},context_instance=RequestContext(request))


def forgot_password(request):
    if not request.user.is_authenticated():
        form = myforms.ForgotForm(request.POST)
        if form.is_valid():
        #user = User.objects.get(username = request.POST["username"])
#            mail_subject = "Reset Your Password"
#            
#            mail_body = '<p>Hello,</p>'
##            mail_body += '<p>You received this email because a Password Reset was requested for your Socialray account.
#            <br />'
#            mail_body += 'Just click the link <a href="' + config.server_base_url + '/resetpassword.htm?' + \'passwordChangeKey=' + uniqueId + '"><strong>Reset My Password</strong></a> to change your password.</p>'
#            mail_body += '<p>If you did not request it, you can safely ignore this mail.</p>'
#            mail_body += '<p>Regards,<br />from Socialray</p>'            
#            mailman.sendOneWayMail(config.system_email,[target_acct.email], mail_subject, mail_body)

            return HttpResponse("Your email address is asd`")
        else:
            form = myforms.ForgotForm()      
            return render_to_response('forget.html',{'form':form},context_instance=RequestContext(request))
            #return HttpResponseRedirect('/login')

