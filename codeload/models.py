from django.db import models

# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_text = models.TextField()

class Solutions(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    source = models.FileField(upload_to='uploads/')
    
