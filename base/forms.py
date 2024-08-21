from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserForm(forms.ModelForm):
    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'JohnDoe123'}),
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john123@email.com'}),
    )
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}), 
        required=True,        
    )
    password2 = forms.CharField(
        label='Password Confirmation', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}), 
        required=True,        
    )

    usable_password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if CustomUser.objects.filter(email=email).exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email

class UserAddressForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First name',
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
    )
    last_name = forms.CharField(
        label='Last name',
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
    )
    phone_number = forms.CharField(
        label='Phone number',
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456789'}),
    )
    address = forms.CharField(
        label='Address',
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New York, NY 10004, US'}),
    )

    usable_password = None

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'address')