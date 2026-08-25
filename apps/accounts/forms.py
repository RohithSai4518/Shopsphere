from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Address, UserPreference

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'role']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-control', 'placeholder': 'Email Address'}),
            'first_name': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Phone Number (Optional)'}),
            'role': forms.Select(attrs={'class': 'input-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-control', 'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-control', 'placeholder': 'Password'}))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'street_address_1', 'street_address_2', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Full Name'}),
            'street_address_1': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Street Address Line 1'}),
            'street_address_2': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Apartment, Suite, etc. (Optional)'}),
            'city': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'State / Province'}),
            'postal_code': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Country'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
        }
