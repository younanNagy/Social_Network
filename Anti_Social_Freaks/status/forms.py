from django import forms


class StatusForm(forms.Form):
    status = forms.CharField()