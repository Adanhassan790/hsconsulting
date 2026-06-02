from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ClientRegistrationForm(UserCreationForm):
    """Client registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'name@company.com',
            'username': 'Choose a username',
            'password1': 'Create a strong password',
            'password2': 'Repeat your password',
        }

        for field_name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_classes + ' form-control').strip()
            field.widget.attrs['placeholder'] = field_placeholders.get(field_name, '')
            field.widget.attrs['autocomplete'] = 'off'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
