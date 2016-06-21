from django.shortcuts import render, get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from .forms import *


@csrf_exempt
def index(request):
    latest_question_list = Recipe.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'recipes_site/index.html', context)


@csrf_exempt
def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    parameters = {'recipe': recipe, 'moment': Quantity.objects.filter(moment=recipe.moments.first())}
    return render(request, 'recipes_site/detail.html', parameters)


@csrf_exempt
def instructions(request, moment_id):
    moment = get_object_or_404(Moment, pk=moment_id)
    parameters = {'moment': moment, 'quantities': Quantity.objects.filter(moment=moment)}
    return render(request, 'recipes_site/instructions.html', parameters)


@csrf_exempt
def create_recipe(request):
    form = RecipeForm()
    mforms = [MomentForm(prefix=str(x), instance=Moment()) for x in range(0,1)]
    return render(request, 'recipes_site/addRecipe.html', {'form': form, 'moments': mforms, 'ingredients': Ingredient.objects.all()})


@csrf_exempt
def create_quantity(request, quantity_id):
    return render(request, 'recipes_site/addQuantity.html', {'name': 'Quantity', 'form': QuantityForm()})


@csrf_exempt
def create_moment(request, moment_id):
    return render(request, 'recipes_site/addMoment.html', {'name': 'Moment', 'id': moment_id, 'form': MomentForm(prefix=str(moment_id))})
