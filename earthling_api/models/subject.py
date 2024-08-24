from django.db import models

class Subject(models.Model):
    age = models.IntegerField()
    native_language = models.CharField(max_length=100)
    other_languages = models.TextField()
    additional_info = models.TextField(blank=True)
