from django.conf.urls import url

from . import views


app_name="recipes_site"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^instructions/(?P<moment_id>[0-9]+)/$', views.instructions, name='instructions'),
    url(r'^addrecipe/$', views.create_recipe, name='add-recipe'),
    url(r'^addquantity/(?P<quantity_id>[0-9]+)/$', views.create_quantity, name='add-quantity'),
    url(r'^addmoment/(?P<moment_id>[0-9]+)/$', views.create_moment, name='add-moment'),
]
