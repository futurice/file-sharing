from django import forms

class PasswordForm(forms.Form):
    password = forms.CharField(max_length=40, widget=forms.PasswordInput())
    filename = forms.CharField(max_length=20, widget=forms.HiddenInput())
