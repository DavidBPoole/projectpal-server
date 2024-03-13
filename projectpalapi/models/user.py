from django.db import models

class User(models.Model):
  name = models.CharField(max_length=55)
  bio = models.TextField()
  uid = models.CharField(max_length=55)
