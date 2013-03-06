from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class UserProfile(models.Model):
    profile=models.ForeignKey(User, unique='true')
    user_type=models.CharField(max_length="10")


class Patient(models.Model):
    user=models.OneToOneField(User)
    contact_no=models.IntegerField()

class Doctor(models.Model):
    user=models.OneToOneField(User)
    speciality=models.CharField(max_length="20")
    availability=models.CharField(max_length="20")
    consult_hour=models.CharField(max_length="30")
    address=models.CharField(max_length="100")

class Slot(models.Model):
    user=models.ForeignKey(User)
    doctor=models.ForeignKey(Doctor)
    Day=(
            ("Monday","MONDAY"),
            ("Tuesday","TUESDAY"),
            ("Wednesday","WEDNESDAY"),
            ("Thursday","THURSDAY"),
            ("Friday","FRIDAY"),
            ("Saturday","SATURDAY"),
            )
    Hour=(
            ("10-12","10-12"),
            ("5-7","5-7"),
            ("5-8","5-8"),
            ("6-9","6-9"),
            )
    day=models.CharField(choices=Day,max_length="20")
    hour=models.CharField(choices=Hour,max_length="20")

class Vote(models.Model):
	user=models.ForeignKey(User)
	vote=models.IntegerField(default= 0, null='true')



