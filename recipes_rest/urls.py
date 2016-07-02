from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from .views import *

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'quantities', QuantityViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'moments', MomentViewSet)
router.register(r'momentfilter', QuantitySearch)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
