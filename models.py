from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    is_counter = models.BooleanField()
    is_student = models.BooleanField()

class PasswordCHangeRequest(models.Model):
    account  = models.ForeignKey(User)
    req_random_key = models.CharField(max_length = 48)
    created_at = models.DateTimeField()

class BalanceAccount(models.Model):
    account  = models.ForeignKey(User)
    counter1_balance = models.IntegerField()
    counter2_balance = models.IntegerField()
    counter3_balance = models.IntegerField()

class Dishes(models.Model):
    dish_id = models.IntegerField(primary_key = True)
    dish_name = models.CharField(max_length = 40)
    dish_price = models.IntegerField()

class Counter(models.Model):
    account = models.ForeignKey(User)

