from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ops', 'Operation User'),
        ('client', 'Client User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"



class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)