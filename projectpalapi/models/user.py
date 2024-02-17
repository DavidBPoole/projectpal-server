from django.db import models

class User(models.Model):
  name = models.CharField(max_length=55)
  uid = models.CharField(max_length=55)
