# Generated by Django 4.2.11 on 2024-04-19 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_app', '0005_alter_recipe_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipes_app.categories'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RecipeCategory',
        ),
    ]
