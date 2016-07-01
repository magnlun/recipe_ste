from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden

from .auth import JWTAuth

import requests

from .forms import *


@csrf_exempt
def index(request):
    token = request.COOKIES.get('token')
    if not token:
        return login(request)
    recipe_get = requests.get(
        "http://localhost:8000/rest/recipes/", auth=JWTAuth(token))
    if recipe_get.status_code >= 400:
        return login(request)
    return render(request, 'recipes_site/index.html', {'recipes': recipe_get.json()})


@csrf_exempt
def detail(request, recipe_id):
    token = request.COOKIES.get('token')
    if not token:
        return login(request)
    recipe_get = requests.get(
        "http://localhost:8000/rest/recipes/" + recipe_id + "/", auth=JWTAuth(token))
    if recipe_get.status_code >= 400:
        return login(request)
    recipe = recipe_get.json()
    parameters = {'recipe': recipe,
                  'moment': recipe["moments"][0]}
    return render(request, 'recipes_site/detail.html', parameters)


@csrf_exempt
def instructions(request, moment_id):
    token = request.COOKIES.get('token')
    if not token:
        return login(request)
    recipe_get = requests.get(
        "http://localhost:8000/rest/moments/" + moment_id + "/", auth=JWTAuth(token))
    if recipe_get.status_code >= 400:
        return login(request)
    moment = recipe_get.json()
    parameters = {'moment': moment, 'recipe': moment}
    return render(request, 'recipes_site/instructions.html', parameters)


@csrf_exempt
def create_recipe(request):
    token = request.COOKIES.get('token')
    if not token:
        return login(request)
    recipe_get = requests.options(
        "http://localhost:8000/rest/recipes/", auth=JWTAuth(token))
    if recipe_get.status_code >= 400:
        return login(request)
    time_units = [k["display_name"] for k in recipe_get.json()["actions"]["POST"]["time_unit"]["choices"]]
    categories = [k["display_name"] for k in recipe_get.json()["actions"]["POST"]["category"]["choices"]]
    ingredients = [k["display_name"] for k in recipe_get.json()["actions"]["POST"]["moments"]["child"]
    ["children"]["ingredients"]["child"]["children"]["ingredient"]["choices"]]

    form = RecipeForm(time_units,categories)
    moment = MomentForm(ingredients=ingredients)
    return render(request, 'recipes_site/addRecipe.html', {'form': form, 'moment': moment})


@csrf_exempt
def create_quantity(request):
    token = request.COOKIES.get('token')
    if not token:
        return HttpResponseForbidden()
    recipe_get = requests.options(
        "http://localhost:8000/rest/quantities/", auth=JWTAuth(token))
    if recipe_get.status_code >= 400:
        return HttpResponseForbidden()
    ingredients = [k["value"] for k in recipe_get.json()["actions"]["POST"]["ingredient"]["choices"]]
    return render(request, 'recipes_site/addQuantity.html', {'name': 'Quantity', 'form': QuantityForm(ingredients=ingredients)})


@csrf_exempt
def create_moment(request):
    token = request.COOKIES.get('token')
    if not token:
        return HttpResponseForbidden()
    recipe_get = requests.options(
        "http://localhost:8000/rest/moments/", auth=JWTAuth(token))
    if recipe_get.status_code >= 400:
        return HttpResponseForbidden()
    ingredients = [k["value"] for k in recipe_get.json()["actions"]["POST"]["extra_ingredients"]["choices"]]

    return render(request, 'recipes_site/addMoment.html', {'name': 'Moment', 'form': MomentForm(ingredients)})

@csrf_exempt
def login(request):
    return render(request, 'recipes_site/login.html')
