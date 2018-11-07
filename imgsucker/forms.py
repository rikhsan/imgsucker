from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, TextInput, NumberInput, EmailInput, Select, PasswordInput, FileInput, ImageField, ClearableFileInput, ChoiceField, HiddenInput
from imgsucker.models import Wallpaper, User

class LoginAdminForm(forms.Form):
    username = forms.CharField(label='user', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'blank': True}))
    password = forms.CharField(label='lock', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'blank': True}))

class LoginClientForm(forms.Form):
	username = forms.CharField(label='envelope', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'blank': True}))
	password = forms.CharField(label='lock', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'blank': True}))

# class RegisterClientForm(forms.Form):
# 	username = forms.CharField(label='user', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'blank': True, 'autocomplete': 'off'}))
# 	email = forms.CharField(label='envelope', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'blank': True, 'autocomplete': 'off'}))
# 	first_name = forms.CharField(label='envelope', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'blank': True, 'autocomplete': 'off'}))
# 	last_name = forms.CharField(label='envelope', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'blank': True, 'autocomplete': 'off'}))
# 	password = forms.CharField(label='lock', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'blank': True, 'autocomplete': 'off'}))

class RegisterClientForm(ModelForm):
	class Meta:
	    model = User
	    fields = ['username', 'email', 'password']
	    labels = {
	   		'username': 'user',
	        'email': 'envelope',
	        # 'first_name': 'envelope',
	        # 'last_name': 'envelope',
	        'password': 'lock',
	    }
	    widgets = {
	    	'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}),
	        'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}),
	        'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
	    }

class EditClientForm(ModelForm):
	class Meta:
	    model = User
	    fields = ['email', 'first_name', 'last_name', 'avatar']

	    widgets = {
	        'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}),
	        'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'autocomplete': 'off'}),
	        'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'autocomplete': 'off'}),
	        # 'avatar': FileInput(attrs={'class': 'custom-file', 'placeholder': 'Avatar', 'autocomplete': 'off'}),
	    }


class GrabForm(forms.Form):
	keywords = forms.CharField(label='Keyword(s)', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keyword(s)', 'blank': True, 'autocomplete': 'off'}))
	specific_site = forms.CharField(label='Specific Site', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specific Site', 'blank': True}))
	limit = forms.IntegerField(label='Limit', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Limit', 'blank': True, 'value': 5}))
	offset = forms.IntegerField(label='Offset', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Offset', 'blank': True, 'value': 0}))
	size_c = (
		('', '-size-'),
		('large', 'large'),
		('medium', 'medium'),
		('icon', 'icon'),
		('>400*300', '>400*300'),
		('>640*480', '>640*480'),
		('>800*600', '>800*600'),
		('>1024*768', '>1024*768'),
		('>2MP', '>2MP'),
		('>4MP', '>4MP'),
		('>6MP', '>6MP'),
		('>8MP', '>8MP'),
		('>10MP', '>10MP'),
		('>12MP', '>12MP'),
		('>15MP', '>15MP'),
		('>20MP', '>20MP'),
		('>40MP', '>40MP'),
		('>70MP', '>70MP'),
		)
	size = forms.CharField(label='Size', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Size', 'blank': True},choices=size_c))

class ModelWallpaperForm(ModelForm):
	tags = forms.CharField(label='Tag(s)', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag(s)', 'blank': True, 'autocomplete': 'off', 'data-role':'tagsinput'}))
	keywords = forms.CharField(label='Keyword(s)', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keyword(s)', 'blank': True, 'autocomplete': 'off', 'readonly':'readonly'}))
	class Meta:
	    model = Wallpaper
	    fields = ['source', 'link', 'uploader','category', 'status']
	    widgets = {
	        'source': TextInput(attrs={'class': 'form-control', 'placeholder': 'Source', 'autocomplete': 'off', 'readonly':'readonly'}),
	        'link': TextInput(attrs={'class': 'form-control', 'placeholder': 'Link', 'autocomplete': 'off', 'readonly':'readonly'}),
	        # 'colors': TextInput(attrs={'class': 'form-control', 'placeholder': 'Colors', 'autocomplete': 'off', 'readonly':'readonly'}),
	        'uploader': Select(attrs={'class': 'form-control', 'placeholder': 'Uploader', 'autocomplete': 'off'}),
	        'category': Select(attrs={'class': 'form-control', 'placeholder': 'Category', 'autocomplete': 'off'}),
	        'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status', 'autocomplete': 'off'}),
	    }


