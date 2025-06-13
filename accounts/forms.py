from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import SetPasswordForm

class CustomUserCreationForm(UserCreationForm):
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    email = forms.EmailField(max_length=254, required=True)
    

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name',  'email',   'password1', 'password2')

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Vérifier si l'email existe déjà dans la base de données
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un compte avec cet email existe déjà.")
        return email


class PasswordResetRequestForm(forms.Form):
    last_name = forms.CharField(label="Nom", max_length=150)
    email = forms.EmailField(label="Adresse email")

    def clean(self):
        cleaned_data = super().clean()
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        if not User.objects.filter(last_name=last_name, email=email).exists():
            raise forms.ValidationError("Aucun utilisateur ne correspond à ce nom et cet email.")
        
        return cleaned_data



class NouveauMotDePasseForm(SetPasswordForm):
    pass  # Inutile de modifier, Django le gère bien


