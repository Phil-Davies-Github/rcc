from django.contrib import admin
from .models import Object1, Object2, Intermediate, ItemModel
# Register your models here.
admin.site.register(ItemModel)
admin.site.register(Object1)
admin.site.register(Object2)
admin.site.register(Intermediate)