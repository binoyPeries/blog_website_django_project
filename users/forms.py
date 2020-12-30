from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# this is used to add additional data to the created from (additioanl fields )
# within brackets what we put is what this class inherits
class UserRegisterForm(UserCreationForm):
    # these are additional fields which are not in the inherited class
    email = forms.EmailField()

    class Meta:
        # what model we are working with(table)
        model = User
        # what fields inside it
        fields = ['username', 'email', 'password1', 'password2']


# model form- this allows us to create a form that works with a specific database model

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email' ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields =['image']

