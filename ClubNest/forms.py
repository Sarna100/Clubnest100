from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email']
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'department', 'semester', 'clubs']
        widgets = {
            'clubs': forms.CheckboxSelectMultiple(),
        }


