from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_text = models.TextField()
    test_file = models.FileField(upload_to='solution_tests/', null=True)

class Solutions(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.FileField(upload_to='uploads/', null=True)
    tests_passed = models.IntegerField(default = 0)
