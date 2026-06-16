from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments"""

    appointment_date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )
    service = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.services.models import Service
        self.fields['service'].queryset = Service.objects.filter(is_active=True)

    class Meta:
        model = Appointment
        fields = ['client_name', 'client_email', 'client_phone', 'service', 'appointment_date', 'message']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (e.g., +254712345678)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your needs...',
                'rows': 4
            }),
        }
