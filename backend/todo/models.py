from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user_email=models.CharField(max_length=120,default='sample_email@gmail.com')
    def _str_(self):
        return self.title