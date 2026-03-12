
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self) -> str:
        return self.name

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Course(BaseModel):
    subject = models.CharField(max_length=100)
    description = models.TextField(null=True) #default null = False
    image = models.ImageField(default=None, null=True)

    category = models.ForeignKey(to=Category,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.subject
    
class Lession(BaseModel):
    subject = models.CharField(max_length=100)
    content = models.TextField(null=True)
    course = models.ForeignKey(to=Course,on_delete=models.RESTRICT)
    tags = models.ManyToManyField(to='Tag',null=True)

class Tag(BaseModel):
    name = models.CharField(max_length=50)
    
from datetime import datetime
class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')



 