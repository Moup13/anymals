from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=300,default = '')
    image = models.ImageField(default="profile1.png", null=True, blank=True)
    cost=models.CharField(max_length=30,default = '')

    description=models.CharField(max_length=5000,default = '')

    def __str__(self):
        return str(self.name)


class News(models.Model):
    image = models.ImageField(default="profile1.png", null=True, blank=True)
    name = models.CharField(max_length=30,default = '')
    description = models.CharField(max_length=5000, default='')


    def __str__(self):
        return str(self.name)




class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000,default = '')
    name = models.CharField(max_length=30,default = '')
    email = models.CharField(max_length=30,default = '')


    def __str__(self):
        return str(self.product)
