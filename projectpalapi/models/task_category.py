from django.db import models
from .task import Task
from .category import Category

class TaskCategory(models.Model):
    task = models.ForeignKey(Task, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='tasks', on_delete=models.CASCADE)
