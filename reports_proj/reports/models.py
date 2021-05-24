from django.db import models
from profiles.models import Profile
from django.shortcuts import reverse
# Create your models here.

class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='reports', blank=True) # for charts we will generate (date from - date to)
    remarks = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('reports:detail', kwargs={'pk': self.pk}) #need to refer to particular path and name as in views.py

    class Meta:
        ordering = ('-created',)