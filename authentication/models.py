from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
gender_type = (
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other")
)
user_type=(
    ("Primary","Primary"),
    ("Seconary","Seconary"),
)
class User(AbstractUser):
    first_name=models.CharField(null=False,max_length=80)
    last_name=models.CharField(null=False,max_length=80)
    dob=models.DateField(null=True)
    gender=models.CharField(default="Male",null=False,choices=gender_type,max_length=10)
    email = models.EmailField(unique=True,null=False)
    mobile = models.CharField(max_length=10,null=False, unique=True)
    user_type=models.CharField(default='Primary',null=False,choices=user_type,max_length=10)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'dob']
    def save(self, *args, **kwargs):
        self.username = str(uuid.uuid1())
        super(User, self).save(*args, **kwargs)