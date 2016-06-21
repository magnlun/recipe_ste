import django_filters
from rest_framework import filters

from recipes_models.models import Recipe


class RecipeFilter(filters.FilterSet):
    max_time = django_filters.NumberFilter(lookup_type='lte', name='sec_time')

    class Meta:
        model = Recipe
        fields = ['max_time']
