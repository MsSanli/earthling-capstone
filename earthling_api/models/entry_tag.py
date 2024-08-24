from django.db import models
from .entry import Entry
from .tag import Tag

class EntryTag(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
