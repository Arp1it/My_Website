from django.contrib import admin
from . models import Contact, userProfile, Codddeee

# Register your models here.
admin.site.register((Contact, userProfile, Codddeee))