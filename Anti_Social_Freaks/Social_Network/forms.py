from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'password1',
                  'password2'
        )
        #then have to define a function that allows the form to save the data to the model.



    def save(self, commit=True):


        try:
            user = super(RegistrationForm,self).save(commit = False)

        except ValueError:
            raise forms.ValidationError("This Username is already taken or Password does not match")




        if commit:
            user.save()





class postForm(forms.Form):
    post = forms.CharField(max_length=2000)



class commentForm(forms.Form):
    comment = forms.CharField(max_length=1000)




class searchForm(forms.Form):
    username = forms.CharField(max_length=150)
