from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'name', 'age', 'gender', 'years_of_exp', 'phone_number',
            'email', 'current_salary', 'expected_salary'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'age': forms.NumberInput(attrs={'min': 0}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'years_of_exp': forms.NumberInput(attrs={'min': 0}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'current_salary': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'expected_salary': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }
        labels = {
            'name': 'Full Name',
            'age': 'Age',
            'gender': 'Gender',
            'years_of_exp': 'Years of Experience',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'current_salary': 'Current Salary',
            'expected_salary': 'Expected Salary',
        }
        help_texts = {
            'age': 'Enter the candidate\'s age.',
            'years_of_exp': 'Enter the total years of experience.',
            'phone_number': 'Enter a valid phone number.',
            'email': 'Enter a valid email address.',
            'current_salary': 'Enter the current salary in numeric value.',
            'expected_salary': 'Enter the expected salary in numeric value.',
        }
