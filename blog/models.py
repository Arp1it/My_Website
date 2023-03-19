from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=20)
    mainhead = models.CharField(max_length=50)
    content = models.TextField(null=False)
    slugg = models.CharField(max_length=100)
    aboutauthor = models.CharField(max_length=50)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.author} - {self.mainhead}"

class Blogcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.comment[0:5]}... by {self.user.username}"