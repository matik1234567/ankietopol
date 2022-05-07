from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
	# username = forms.CharField(widget=forms.TextInput(attrs={'class': 'field-sm'}))
	class Meta:
		model = User
		fields = ['username', 'first_name', 'email', 'password1', 'password2']
