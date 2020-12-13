from django.db import models

# Create your models here.

class ContactFormData(models.Model):
    subject = models.CharField(max_length=50)
    message = models.TextField()
