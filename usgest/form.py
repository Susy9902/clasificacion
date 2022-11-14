from django import forms

class LoginForm(forms.Form):

    usuario = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput())

class ResgisterForm(forms.Form):
    usuario = forms.CharField(max_length=50, required = True)
    Name = forms.CharField(max_length=50)
    Lastname = forms.CharField(max_length=50)
    email = forms.EmailField(widget = forms.EmailInput(), required = True)
    contraseña = forms.CharField(widget=forms.PasswordInput(), required = True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required = True)
