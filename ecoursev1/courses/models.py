

from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField

# Create your models here.
class User(AbstractUser):
    pass

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self) -> str:
        return self.name
    
class Course(BaseModel):
    subject = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField(null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.subject

class Lesson(BaseModel):
    subject = models.CharField(max_length=100)
    content = RichTextField()
    image = CloudinaryField(null=True)
    
    def __str__(self) -> str:
        return self.subject



    
