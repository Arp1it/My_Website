from django.contrib import admin
from . models import Contact, userProfile

# Register your models here.
admin.site.register((Contact, userProfile))