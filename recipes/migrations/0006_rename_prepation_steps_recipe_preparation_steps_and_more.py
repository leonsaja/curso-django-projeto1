# Generated by Django 4.1.4 on 2023-01-09 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='prepation_steps',
            new_name='preparation_steps',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='prepation_steps_is_html',
            new_name='preparation_steps_is_html',
        ),
    ]