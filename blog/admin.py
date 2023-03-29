from django.contrib import admin
from . models import BlogPost, Blogcomment, BlogLike, BlogViews

# Register your models here.
admin.site.register((BlogPost, Blogcomment, BlogLike, BlogViews))