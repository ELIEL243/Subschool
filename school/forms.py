from django import forms
from django.forms import ModelForm


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'label': ''
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Nom'
        self.fields['password'].label = 'Mot de passe'
        self.fields['username'].widget.attrs['placeholder'] = "nom d'utilisateur"
        self.fields['password'].widget.attrs['placeholder'] = 'mot de passe'


class HomeWorkForm(ModelForm):
    class Meta:
        fields = ['']
