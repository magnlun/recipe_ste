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
        return False
    recipeGet = requests.get("http://localhost:8000/rest/recipes/", auth=
    JWTAuth(token))
    if recipeGet.status_code >= 400:
        return False
    return render(request, 'recipes_site/index.html', {'recipes': recipeGet.json()})


@csrf_exempt
def detail(request, recipe_id):
    token = request.COOKIES.get('token')
    if not token:
        return False
    recipeGet = requests.get("http://localhost:8000/rest/recipes/" + recipe_id + "/", auth=
    JWTAuth(token))
    if recipeGet.status_code >= 400:
        return login(request)
    recipe = recipeGet.json()
    parameters = {'recipe': recipe,
                  'moment': recipe["moments"][0]}
    return render(request, 'recipes_site/detail.html', parameters)


@csrf_exempt
def instructions(request, moment_id):
    token = request.COOKIES.get('token')
    if not token:
        return False
    recipeGet = requests.get("http://localhost:8000/rest/moments/" + moment_id +"/", auth=
    JWTAuth(token))
    if recipeGet.status_code >= 400:
        return login(request)
    moment = recipeGet.json()
    parameters = {'moment': moment}
    return render(request, 'recipes_site/instructions.html', parameters)


@csrf_exempt
def create_recipe(request):
    if not logged_in(request):
        return login(request)
    form = RecipeForm()
    moment = MomentForm()
    return render(request, 'recipes_site/addRecipe.html', {'form': form, 'moment': moment, 'ingredients': Ingredient.objects.all()})


@csrf_exempt
def create_quantity(request):
    if not logged_in(request):
        return login(request)
    return render(request, 'recipes_site/addQuantity.html', {'name': 'Quantity', 'form': QuantityForm()})


@csrf_exempt
def create_moment(request):
    token = request.COOKIES.get('token')
    if not token:
        return False
    recipeGet = requests.options("http://localhost:8000/rest/recipes/", auth=
    JWTAuth(token))
    if recipeGet.status_code >= 400:
        return HttpResponseForbidden()
    return render(request, 'recipes_site/addMoment.html', {'name': 'Moment', 'form': MomentForm()})

@csrf_exempt
def login(request):
    return render(request, 'recipes_site/login.html')


def logged_in(request):
    token = request.COOKIES.get('token')
    if not token:
        return False
    recipeGet = requests.get("http://localhost:8000/rest/recipes/", auth=
    JWTAuth(token))
    if recipeGet.status_code >= 400:
        return False
    return True
