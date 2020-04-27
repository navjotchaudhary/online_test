from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    has_details = models.BooleanField(default=False)
    about = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='profile_image',blank = True, null = True)
    website = models.CharField(max_length=40)





