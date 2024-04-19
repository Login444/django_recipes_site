from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField(max_length=800)
    steps = models.TextField(max_length=2000)
    cooking_time = models.IntegerField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title




class RecipeCategory(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe.title} - {self.category.name}'

