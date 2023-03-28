from django.db import models

from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
import uuid
from datetime import datetime



# Create your models here.







class imag(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(null=True)
    def __str__(self):
        return self.user.username


class comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    img=models.ForeignKey(imag,on_delete=models.CASCADE)
    comment=models.TextField()
    def __str__(self):
        return self.user.username
    

