# Create your views here.

from django.shortcuts import render_to_response
from pycourt_login.complaint.forms import ComplaintForm
from django.http import HttpResponse,HttpResponseRedirect

def complaint(request):
	if request.method == 'POST':
		form = ComplaintForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			message_body=cd['counter']+": "+cd['description']
			"""send_mail(
				cd['subject'],
				message_body,
				'200801066@daiict.ac.in',
				['cmc@daiict.ac.in'], fail_silently=False)"""
			return HttpResponseRedirect('/home')
	else:
		form = ComplaintForm()
	return render_to_response('complaint_form.html', {'form': form})
