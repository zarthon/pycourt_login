from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decoraters import login_required 
from django.contrib.auth.models import User
from django.http import HttpRespons, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
'''Import forms and User profile'''

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/logout')
    else:
        return HttpResponseRedirect('/login')

def login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            forms = myforms.LoginForm(request.POST)
            if form.is_valid():
                u = form.cleaned_data['username']
                e = form.cleaned_data['email']
                p = form.cleaned_data['password']
                print p
                user = authenticate(username=e,password=p)
                if user is not None:
                    auth_login(request,user)
                    return HttpResponseRedirect('/logout/')
                else:
                    return HttpResponse('fail')
        else:
            form = myforms.LoginForm()      
            return render_to_response('login.html',{'form':form}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def logout(request): 
    auth_logout(request)
    return HttpResponseRedirect('/login/')

def register(register):
    if not request.user.is_authenticated():
        if request.method == 'POST'
            form = myforms.RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username = request.POST["username"],password=request.POST["password"])
                auth_login(request,user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response("signup.html",{'signup_form':signup_form,'signup':True,'data':request.POST})


        
