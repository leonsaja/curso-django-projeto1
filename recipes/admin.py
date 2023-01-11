from django.contrib import admin

from .models import Category, Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display='id','title','created_at','is_published',
    list_filter='is_published','category','author',
    list_display_links='title','created_at'
    search_fields='id','title','description','slug',
    list_editable='is_published',
    prepopulated_fields={
        "slug":('title',)
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
