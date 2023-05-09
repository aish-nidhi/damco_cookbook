from django.db import models
from recipes.models import Recipe

# Create your models here.

class Ingredients(models.Model):

    name = models.CharField(max_length=100)

class IngredientRecipeMapping(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    comments = models.CharField(max_length=500, null=True)
    alternate_ingredient = models.CharField(max_length=50, null=True)
    quantity = models.CharField(max_length=9, null=True)
    measuring_unit = models.CharField(max_length=20, null=True)