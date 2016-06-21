from django.forms import ModelForm
from django import forms
from recipes_models.models import Recipe, Moment, Quantity, Ingredient
from itertools import chain


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('creator',)


class MomentForm(ModelForm):
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

    def __init__(self):
        set = list(chain((('',''), ), Ingredient.objects.values_list('id', 'name')))
        settings = {'data-placeholder':'Choose an ingredient','class':'chosen-select',}
        self.ingredient = forms.ChoiceField()
        self.ingredient.widget = forms.Select(choices=set,
                                     attrs=settings)
        super().__init__();

    class Meta:
        model = Quantity
        fields = ('amount','unit','ingredient','comment',)

