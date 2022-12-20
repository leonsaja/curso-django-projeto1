from django.contrib import admin

from .models import Category, Recipe


class RecipeAdmin(admin.ModelAdmin):
    pass    

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recipe)
admin.site.register(Category)