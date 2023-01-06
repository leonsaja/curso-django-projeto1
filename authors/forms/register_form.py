from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password2=forms.CharField(label='Confirmer a Senha:', required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer a senha'}))
    password=forms.CharField(label='Senha:',required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Digite a sua senha'}))
    
    class Meta:
        model=User
        fields= ['first_name','last_name','username', 'email','password']

        labels={
            'email':'E-mail:',
            'first_name':'Nome:',
            'last_name':'Sobrenome:',
        }
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
            raise ValidationError({'password2':'As senhas precisam ser iguais !'})
        
      
       