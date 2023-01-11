from django.contrib import messages
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination, make_pagination_range

from .models import Recipe

PER_PAGE=9
def home(request):
    
    recipes=Recipe.objects.filter(is_published=True)
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    messages.success(request, 'Seja Bem Vindo ao Site de Receita !')
    return render(request,'recipes/pages/home.html',context={
        "recipes":page_obj,
        "pagination_range":pagination_range,
        
    })


def search(request):
    search_term=request.GET.get('q','').strip()
    
    if not search_term:
        raise Http404()

    recipes=Recipe.objects.filter((
    Q(title__icontains=search_term) |
    Q(description__icontains=search_term)
    ),is_published=True)
    
    page_obj, pagination_range = make_pagination(request, recipes, 9)


    return render(request, 'recipes/pages/search.html', context={
        
        'search':search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })

def category(request,category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        # 'title': f'{recipes.first().category.name} | Category'                'pagination_range': pagination_range,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} | Category',
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
