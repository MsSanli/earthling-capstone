from django.db import models
from .subject import Subject
from .user import User
from .tag import Tag
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField()
    ipa_text = models.CharField(max_length=255)
    meaning = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name='entries', blank=True)
