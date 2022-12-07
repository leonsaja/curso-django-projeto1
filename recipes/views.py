from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request,'recipes/pages/home.html',context={'nome':'Olá Mundo !!!'})




def recipe(request, id):
    return render (request, 'recipes/pages/recipe-view.html', context=
    {'recipe': 'Café da amanha'})
    