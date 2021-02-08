from django.db import models
from users.models import CustomUser

class Course(models.Model):
    instructor = models.ForeignKey(CustomUser, related_name='courses', on_delete=models.CASCADE,blank=True ,null=True)
    name = models.CharField(default ="",null = False,blank=False,max_length=50)
    credit = models.IntegerField(null = False,blank=False)
    is_essential = models.BooleanField(default=True)
    students = models.ManyToManyField(CustomUser, related_name='courselist',blank=True)

class Class(models.Model):
    name = models.CharField(default ="",null = False,blank=False,max_length=50)
    students = models.ManyToManyField(CustomUser, related_name='level',blank=True)
    def __str__(self):
        return self.name
    
