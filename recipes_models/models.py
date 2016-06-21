from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class TimeUnit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    seconds = models.IntegerField()

    def sec(self):
        return self.seconds

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name='recipes')
    time = models.IntegerField()
    time_unit = models.ForeignKey(TimeUnit, on_delete=models.CASCADE)
    source = models.TextField(blank=True)
    category = models.ManyToManyField(Category)
    portions = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'recipes'
        ordering = ['name']

    def owner(self):
        return self.creator

    def __str__(self):
        return self.name


class Moment(models.Model):
    name = models.CharField(max_length=30)
    ingredients = models.ManyToManyField(Ingredient, through='Quantity', related_name="quantities")
    extra_ingredients = models.ManyToManyField(Ingredient, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='moments')
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.recipe.name + "/" + self.name


class Quantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    unit = models.CharField(max_length=10)
    comment = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = 'quantities'

    def owner(self):
        return self.moment.recipe.owner()

    def __str__(self):
        return "{0} {1} {2}".format(self.amount.normalize(), self.unit, self.ingredient.name)
