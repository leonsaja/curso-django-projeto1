from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request,'home.html',context={'nome':'Olá Mundo !!!'})