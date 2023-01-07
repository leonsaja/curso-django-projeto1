import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_form import strong_password


class RegisterForm(forms.ModelForm):
    password=forms.CharField(label='Senha:',required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Digite a sua senha'}))
    password2=forms.CharField(label='Confirmer a Senha:', required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer a senha'}),
    help_text=(
        'A senha deve ter pelo menos uma letra maiúscula, '
           'uma letra minúscula e um número. O comprimento deve ser '
             'pelo menos 8 caracteres.'
     ))
    first_name=forms.CharField(label='Nome:', required=True, )
    last_name=forms.CharField(label='Sobrenome:', required=True)
    email=forms.EmailField(label='E-mail:', required=True)
    username=forms.CharField(label='Usuário', help_text=(
        'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
    ))
    
    class Meta:
        model=User
        fields= ['first_name','last_name','username', 'email','password']

    def clean_email(self):
        data_email=self.cleaned_data.get('email')

        if User.objects.filter(email=data_email).exists():
            raise ValidationError(
                'E-mail já existe !'
            )
        return data_email


    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        password2=cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({'password2':'As senhas precisam ser iguais.'})
        
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
        if not regex.match(password):
            raise ValidationError({'password':'A senha deve ter pelo menos uma letra maiúscula, '
                'uma letra minúscula e um número. O comprimento deve ser '
                'pelo menos 8 caracteres.'})


       