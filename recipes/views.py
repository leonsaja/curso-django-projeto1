from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.recipes.factory import make_recipe

from .models import Category, Recipe


def home(request):
    recipes=Recipe.objects.filter(is_published=True)
    return render(request,'recipes/pages/home.html',context={
        "recipes":recipes
    })


def search(request):
    search_term=request.GET.get('q','').strip()
    
    if not search_term:
        raise Http404()

    recipes=Recipe.objects.filter((
    Q(title__icontains=search_term) |
    Q(description__icontains=search_term)
    ),is_published=True)

    return render(request, 'recipes/pages/search.html', context={
        'recipes':recipes,
        'search':search_term,
    })

def category(request,category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        # 'title': f'{recipes.first().category.name} | Category'
        'title': f'{recipes[0].category.name} - Category | '
    })

def recipe(request, id):
    recipe = Recipe.objects.filter(
        pk=id,
        is_published=True,
    ).order_by('-id').first()

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
