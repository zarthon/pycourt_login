from django import forms

class ComplaintForm(forms.Form):
	subject = forms.CharField()
	counter = forms.CharField(required=False)
	description = forms.CharField(widget=forms.Textarea)
