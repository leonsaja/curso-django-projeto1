from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_form import add_attr
from utils.string import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._my_errors=defaultdict(list)
        

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        # add_attr(self.fields.get('cover'), 'class', 'span-2')
        
    # preparation_steps=forms.CharField(widget=forms.Textarea(attrs={'class':'span-2'}))
    
    class Meta:
        
       
        model=Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover',
        widgets = {
            # 'preparation_steps':forms.Textarea(attrs={'class':'span-2'}),            
            'cover':forms.FileInput(attrs={'class': 'span-2'}),
            'servings_unit':forms.Select(
                choices=(
                
                 ('Porções','Porções'),
                 ('Pedaços','Pedaços'),
                 ('Pessoas','Pessoas'),
                 
                 
                )
            ),
            'preparation_time_unit':forms.Select(
                choices=(
                
                 ('Minutos ','Minutos'),
                 ('Horas','Horas'),
               
                 
                 
                )
            ),
                
            }
    def clean(self,*args, **kwargs):
        super_clean= super().clean(*args,**kwargs)
        cleaned_data=self.cleaned_data
        
        title=cleaned_data.get('title')
        description=cleaned_data.get('description')
        
        if title == description:
            self._my_errors['title'].append('Não pode ser igual à descrição')
            self._my_errors['description'].append('Não pode ser igual ao título')
        
        if self._my_errors:
            raise ValidationError(self._my_errors)
        
        return super_clean
    
    def clean_title(self):
        title=self.cleaned_data.get('title')
            
        if len(title) < 5:
            self._my_errors['title'].append('Deve ter pelo menos 5 caracteres.')
            
        return title
    
    def clean_preparation_time(self):
        preparation_time=self.cleaned_data.get('preparation_time')
        
        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append('Deve ser um número positivo')


        return preparation_time
    
    def clean_servings(self):
        servings=self.cleaned_data.get('servings')
        
        if not is_positive_number(servings):
            self._my_errors['servings'].append('Deve ser um número positivo')

        return servings
        
     
                
        