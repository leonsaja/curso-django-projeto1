from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from authors.forms import login_form, register_form


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form =register_form.RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
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

    return redirect('authors:register')
