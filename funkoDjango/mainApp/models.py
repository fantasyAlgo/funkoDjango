from django.db import models

# Create your models here.
class FunkoPop(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length = 100)
    link_image = models.CharField(max_length = 300)
    cost = models.IntegerField(default=0)
