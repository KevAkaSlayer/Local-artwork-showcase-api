from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
# Create your models here.

class Artist(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='api/images/artist', blank=True, null=True)
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()
    def __str__(self):
        return self.username
    

class Artwork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    artist = models.ForeignKey(Artist,blank=True,default=None,null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='api/images/artworks',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title