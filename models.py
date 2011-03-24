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

class CounterAccount(models.Model):
	account = models.ForeignKey(User)
	balance = models.IntegerField()


class Dishes(models.Model):
	dish_name = models.CharField(max_length = 40)
	dish_price = models.IntegerField()
	counter1 = models.BooleanField()
	counter2 = models.BooleanField()
	counter3 = models.BooleanField()
 
class Order(models.Model):
	order_id = models.CharField(max_length=60)
	student_id = models.ForeignKey(User)
	status = models.BooleanField()
	datetime = models.DateTimeField()
	counterid = models.IntegerField()

