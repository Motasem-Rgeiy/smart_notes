from django.db import models
from django.contrib.auth.models import User , AbstractUser
from django.core.validators import FileExtensionValidator
# Create your models here.

class User(AbstractUser):
    image = models.ImageField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100) #Should be unique per user
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'], 
                name='unique_category_per_user'
            )
        ]

    def __str__(self):
        return self.name

class NoteStatus(models.IntegerChoices):
    NORMAL = 1 , 'normal'
    IMPORTANT = 2 , 'important'
    COMPLETED = 3 , 'completed'

class Note(models.Model):
    title = models.CharField(max_length=100 , null=True , blank=True)
    description = models.TextField()
    status = models.IntegerField(choices=NoteStatus.choices , default=NoteStatus.NORMAL)
    image = models.ImageField(null=True , blank=True)
    uploaded_file = models.FileField( null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['txt' , 'pdf'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True , related_name='notes')
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.title or ' '
