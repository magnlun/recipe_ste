from django.contrib import admin

from .models import *


class QuantityInline(admin.StackedInline):
    model = Quantity
    extra = 5
    fields = ('amount', 'unit', 'ingredient', 'comment',)


class MomentAdmin(admin.ModelAdmin):
    inlines = [QuantityInline]

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(TimeUnit)
admin.site.register(Category)
admin.site.register(Moment, MomentAdmin)
