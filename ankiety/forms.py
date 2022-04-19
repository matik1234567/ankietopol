from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class CreateUserForm(UserCreationForm):
	# username = forms.CharField(widget=forms.TextInput(attrs={'class': 'field-sm'}))
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
