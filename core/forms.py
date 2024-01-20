from django import forms
from django.core.validators import EmailValidator

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"

class DateTimeLocalField(forms.DateTimeField):
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

class MeetingForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, label='Name')
    email = forms.EmailField(label='Email', validators=[EmailValidator()])
    phone_number = forms.CharField(max_length=20, label='Phone Number')
    address = forms.CharField(max_length=255, label='Address')
    
    # Define choices for the "Service Interest" field
    SERVICE_INTEREST_CHOICES = [
        ('SEO', 'SEO'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Web Development', 'Web Development'),
        ('Graphics Design', 'Graphics Design'),
    ]
    
    service_interest = forms.ChoiceField(
        choices=SERVICE_INTEREST_CHOICES,
        label='Service Interest',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True  # Make it required
    )
    
    # Define choices for the "How did you find us?" field
    FIND_US_CHOICES = [
        ('Google', 'Google'),
        ('Youtube', 'Youtube'),
        ('X', 'X'),
        ('Facebook', 'Facebook'),
        ('Linkedin', 'Linkedin'),
        ('Other', 'Other'),
    ]
    
    how_found_us = forms.ChoiceField(
        choices=FIND_US_CHOICES,
        label='How did you find us?',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True  # Make it required
    )
    
    message = forms.CharField(widget=forms.Textarea, label='Message')
