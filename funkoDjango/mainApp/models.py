from django.db import models
from datetime import date

# Create your models here.
class FunkoPop(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length = 100)
    link_image = models.CharField(max_length = 300)
    cost = models.IntegerField(default=0)


class User(models.Model):
    username = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    funkos = models.ManyToManyField(FunkoPop, related_name='funkos')
    wishedFunkos = models.ManyToManyField(FunkoPop, related_name="wishedFunkos")


class Review(models.Model):
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 400)
    stars = models.IntegerField(default=5)
    item = models.ForeignKey(FunkoPop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

