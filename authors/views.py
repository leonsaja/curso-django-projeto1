from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import login_form, recipe_form, register_form
from recipes.models import Recipe


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form =register_form.RegisterForm(register_form_data)
    
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create')
    })
    
    # if request.POST:
    #     form=register_form.RegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('recipes:home')
    #     else:
    #         return render(request,'authors/register.html', {'form':form})
    # else:
    #     return render(request,'authors/register.html', {'form':form})

def register_create(request):

    if  not request.POST:
        raise Http404()

    POST=request.POST
    request.session['register_form_data']=POST
    form=register_form.RegisterForm(POST)


    if form.is_valid():
        user=form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request,'Cadastro realizado com sucesso !')    
        del(request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')

def login_view(request):
    
    form=login_form.LoginForm()
    return render(request,'authors/pages/login.html',{
    'form':form,
    'form_action': reverse('authors:login_create')
    })

def login_create(request):
    
    if not request.POST:
        raise Http404()

    form=login_form.LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username',''),
            password=form.cleaned_data.get('password',''))
    
        if  authenticated_user :
            messages.success(request,'logando com sucesso.')
            login(request, authenticated_user )
        else:
            messages.error(request,' Credencias Inválida.')    
    else:
        messages.error(request, 'Usuario ou Senha Inválida.')
    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login',redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
   
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
  
    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login',redirect_field_name='next')
def dashboard(request):
    recipes=Recipe.objects.filter(is_published=False, author=request.user )
  
    return render(request,'authors/pages/dashboard_view.html',{'recipes':recipes})

@login_required(login_url='authors:login',redirect_field_name='next')
def dashboard_recipe_create(request):
    
    form=recipe_form.AuthorRecipeForm(data=request.POST or None, 
                                      files=request.FILES or None,
                                      )
    if form.is_valid():
       form=form.save(commit=False)
       form.author=request.user
       form.save()
       messages.success(request,'A sua receita foi salvo com sucesso')
       return redirect(reverse('authors:dashboard_recipe_id',args=(form.id,)))
    
    return render(request,'authors/pages/dashboard_create_recipe.html',{'form':form})
    

@login_required(login_url='authors:login',redirect_field_name='next')
def dashboard_recipe_id(request,id):
    recipe=Recipe.objects.get(is_published=False, author=request.user, id=id )
    
    if not recipe:
        raise Http404()

    form=recipe_form.AuthorRecipeForm(data=request.POST or None, 
                                      files=request.FILES or None,
                                      instance=recipe)
    if form.is_valid():
       form=form.save(commit=False)
       form.author=request.user
       form.save()
       messages.success(request,'A sua receita foi salvo com sucesso')
       return redirect(reverse('authors:dashboard_recipe_edit',args=(id,)))
    
    return render(request,'authors/pages/dashboard_recipe.html',{'form':form})
    
