from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    is_not_robot = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must confirm you are not a robot'}
    )

    class Meta:
        model = ContactSubmission
        fields = ['name', 'surname', 'email', 'message', 'is_not_robot']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your First Name'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Email Address'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Your Message',
                'rows': 5
            }),
            'is_not_robot': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }