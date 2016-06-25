from rest_framework import serializers
from rest_framework.metadata import BaseMetadata
from django.db import transaction

from recipes_models.models import *


class IngredientMetadata(BaseMetadata):
    def determine_metadata(self, request, view):
        return {
            'display_name': view.get_view_name(),
            'value': view.id
        }


class IngredientSerializer(serializers.ModelSerializer):
    metadata_class = IngredientMetadata
    class Meta:
        model = Ingredient
        fields = ('id', 'url', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'name',)


class QuantitySerializer(serializers.ModelSerializer):
    ingredient = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = Quantity
        fields = ('amount', 'unit', 'ingredient',)


class MomentSerializer(serializers.ModelSerializer):
    ingredients = QuantitySerializer(source='quantity_set', many=True)
    extra_ingredients = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = Moment
        fields = ('id', 'url', 'name', 'ingredients', 'extra_ingredients', 'instructions', )


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RecipeSerializer(DynamicFieldsModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.username')
    moments = MomentSerializer(many=True)
    time_unit = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=TimeUnit.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=Category.objects.all()
    )

    @transaction.atomic
    def create(self, validated_data, commit=True, *args, **kwargs):
        moments = validated_data.pop('moments')
        categories = validated_data.pop('category')
        recipe = Recipe.objects.create(commit=commit, **validated_data)
        recipe.category = categories
        for jsonMoment in moments:
            quantities = jsonMoment.pop('quantity_set')
            extra_ingredients = jsonMoment.pop('extra_ingredients')
            moment = Moment.objects.create(commit=commit, recipe=recipe, **jsonMoment)
            for ingredient in extra_ingredients:
                moment.extra_ingredients.add(Ingredient.objects.get(name=ingredient))
            for quantity in quantities:
                Quantity.objects.create(commit=commit, moment=moment, **quantity)
            moment.save(commit=commit)
        recipe.save(commit=commit)
        return recipe

    class Meta:
        model = Recipe
        fields = ('id', 'url', 'name', 'description', 'creator', 'time', 'time_unit', 'category', 'moments')


class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'recipes')
