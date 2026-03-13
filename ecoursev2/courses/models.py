from django.db import models
from django.contrib.auth.models import AbstractUser
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

class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Course(BaseModel):
    subject = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField(null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    class Meta:
        unique_together = ('subject','category')
    
    def __str__(self):
        return self.subject
    

class Lession(BaseModel):
    subject = models.CharField(max_length=100)
    content = RichTextField(null=True)
    image = CloudinaryField()
    course = models.ForeignKey(Course,on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.subject
    
class Tag(BaseModel):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Interaction(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    lession = models.ForeignKey(Lession, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.TextField()

class Like(Interaction):
    class Meta:
        unique_together = ('lession','user')
