from django.forms import ModelForm
from django import forms
from recipes_models.models import Recipe, Moment, Quantity, Ingredient
from itertools import chain


class RecipeForm(ModelForm):

    source = forms.CharField()

    def __init__(self, time_units, categories):
        super().__init__()
        self.time_unit = forms.ChoiceField()
        self.time_unit.widget = forms.Select(choices=time_units)
        self.category = forms.ChoiceField()
        self.category.widget = forms.SelectMultiple(choices=categories)

    class Meta:
        model = Recipe
        exclude = ('creator',)


class MomentForm(ModelForm):

    def __init__(self, ingredients):
        self.extra_ingredients = forms.ChoiceField()
        self.extra_ingredients.widget = forms.SelectMultiple(choices=ingredients)
        super().__init__()

    class Meta:
        model = Moment
        exclude = ('recipe','ingredients')


class QuantityForm(ModelForm):

    amount = forms.IntegerField()
    amount.widget = forms.NumberInput(attrs={'name':'amount'})

    unit = forms.CharField()
    unit.widget = forms.TextInput(attrs={'name':'unit'})

    comment = forms.CharField()
    comment.widget = forms.TextInput(attrs={'name':'comment'})

    def __init__(self, ingredients):
        settings = {'data-placeholder':'Choose an ingredient','class':'chosen-select',}
        self.ingredient = forms.ChoiceField()
        self.ingredient.widget = forms.Select(choices=ingredients,
                                     attrs=settings)

        super().__init__()

    class Meta:
        model = Quantity
        fields = ('amount','unit','ingredient','comment',)

