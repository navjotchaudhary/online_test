from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    has_details = models.BooleanField(default=False)
    about = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='main_image',blank = True, null = True)
    website = models.CharField(max_length=40)
    slug = models.SlugField(null=True,blank="true")


    def save(self,*args,**kwargs):
        if not self.slug and self.username:
            self.slug = slugify(self.username)

        super(User,self).save(*args,**kwargs)

class contactUs(models.Model):
    name = models.CharField(max_length = 40)
    email = models.EmailField()
    message = models.TextField(max_length=1000)



    def __str__(self):
        return self.name



