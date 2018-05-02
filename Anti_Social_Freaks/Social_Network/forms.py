from django import forms

class postForm(forms.Form):
    post = forms.CharField(max_length=2000)
