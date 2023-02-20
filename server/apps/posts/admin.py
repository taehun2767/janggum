from django.contrib import admin
from server.apps.posts import models
# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.User)
admin.site.register(models.Comment)
admin.site.register(models.AllUsedIngredient)