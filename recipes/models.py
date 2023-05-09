from django.db import models

# Create your models here.

class Recipe(models.Model):

    VEGETARIAN = "veg"
    NON_VEGETARIAN = "non-veg"

    RECIPE_TYPE = (
        (VEGETARIAN, VEGETARIAN),
        (NON_VEGETARIAN, NON_VEGETARIAN)
    )

    ['index', 'Sl. No', 'PDF Number', 'Recipe Name', 'Alternate Name',
       'Recipe Type', 'Description', 'Meat Type', 'Meat Classification',
       'Cuisine', 'Serving Quantity', 'Serve', 'meal type', 'Cookware',
       'Calories per\nServing'],

    name = models.CharField(max_length=10)
    recipe_type = models.CharField(max_length=10, choices=RECIPE_TYPE)
    alternate_name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500)

    #move meat info to Enum class
    meat_type = models.CharField(max_length=20, null=True)
    meat_classfication = models.CharField(max_length=20, null=True)

    cuisine = models.CharField(max_length=50, null=True)
    serving_quantity = models.CharField(max_length=20, null=True)
    serves = models.CharField(max_length=10, null=True)

    #create choice field after getting all probable choice data
    meal_type = models.CharField(max_length=30, null=True)

    #change to list if time permits
    cookwares = models.CharField(max_length=200, null=True)

class Instructions(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    pre_cooking_steps = models.CharField(max_length=5000, null=True)
    cooking_steps = models.CharField(max_length=5000, null=True)
    tips = models.JSONField(default=dict, null=True)

    #change to integerField
    total_duration = models.CharField(default="30", max_length=5, null=True)