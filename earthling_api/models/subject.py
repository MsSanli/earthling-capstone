from django.db import models
from .language import Language

class Subject(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True)
