from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    message = models.TextField()
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, RELATED_NAME = 'Profile')
#     image = models.ImageField(upload_to="media/mainn/images", default="static/default.webp")