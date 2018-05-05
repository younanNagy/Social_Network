from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2'
        )
        #then have to define a function that allows the form to save the data to the model.



    def save(self, commit=True):


        try:
            user = super(RegistrationForm,self).save(commit = False)
            user.first_name = self.cleaned_data['first_name']
            # cleaned_data--> makes sure that there is no SQL in the data and it's safe to save it.
            user.last_name = self.cleaned_data['last_name']


        except ValueError:
            raise forms.ValidationError("This Username is already taken or Password does not match")




        if commit:
            user.save()





class postForm(forms.Form):
    post = forms.CharField(max_length=2000)



class commentForm(forms.Form):
    comment = forms.CharField(max_length=1000)
