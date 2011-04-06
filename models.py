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

	def __unicode__(self):
		return self.dish_name
	
	def natural_key(self):
		return (self.dish_name)

class Orders(models.Model):
	transaction_id = models.CharField(max_length=30)
	order_id = models.CharField(max_length=60)
	quantity = models.IntegerField()
	dish = models.ForeignKey(Dishes)
	student_id = models.ForeignKey(User)
	status = models.IntegerField()
	delivered = models.BooleanField()
	datetime = models.DateTimeField()
	counterid = models.CharField(max_length=9)

class LoginStatus(models.Model):
	counterid = models.ForeignKey(User)
	status = models.BooleanField()
