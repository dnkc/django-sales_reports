from django.db import models

# Create your models here.

# EACH FIELD IS A COLUMN
# EACH OBJECT IS A ROW IN THE DB TABLE

class Customer(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='customers', default='no_picture.png')