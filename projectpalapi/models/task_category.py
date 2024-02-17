from django.db import models
from .task import Task
from .category import Category

class TaskCategory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
