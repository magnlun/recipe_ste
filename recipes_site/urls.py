from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views


app_name="recipes_site"
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^instructions/(?P<moment_id>[0-9]+)/$', views.instructions, name='instructions'),
    url(r'^addrecipe/$', views.create_recipe, name='add-recipe'),
    url(r'^addquantity/$', views.create_quantity, name='add-quantity'),
    url(r'^addmoment/$', views.create_moment, name='add-moment'),
]
