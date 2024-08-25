from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    number_of_speakers = models.IntegerField()
    pronunciation = models.CharField(max_length=100)
    language_family = models.CharField(max_length=100)
    writing_system = models.CharField(max_length=100)
