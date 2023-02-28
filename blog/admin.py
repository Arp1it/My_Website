from django.contrib import admin
from . models import BlogPost, Blogcomment

# Register your models here.
admin.site.register((BlogPost, Blogcomment))