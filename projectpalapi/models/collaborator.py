from django.db import models
from .user import User
from .project import Project

class Collaborator(models.Model):
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='users', on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
