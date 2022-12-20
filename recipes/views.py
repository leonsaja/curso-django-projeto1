from django.http import HttpResponse
from django.shortcuts import render

from utils.recipes.factory import make_recipe

from .models import Category, Recipe


def home(request):

    recipes=Recipe.objects.all()
    return render(request,'recipes/pages/home.html',context={
        "recipes":recipes
    })
    #     'nome':'Olá Mundo !!!',
    #      'recipes' : [make_recipe() for _ in range(10)],        
        
    #     })

def recipe(request, id ):
    return render(request, 'recipes/pages/recipe-view.html', 
    context={'name': 'Leonardo Pereira', 
    'recipe':make_recipe(),
    'is_detail_page':True,
    
    })
