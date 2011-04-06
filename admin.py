from pycourt_login.models import *
from django.contrib import admin

class DishesAdmin(admin.ModelAdmin):
	list_display = ('id','dish_name','dish_price','counter1','counter2','counter3')
	search_fields = ('dish_name',)

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user','is_counter','is_student')
	search_fields = ('user.username',)
class OrderssAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id','student_id','counterid','transaction_id','delivered')
    search_fields = ('student_id','transaction_id')
class LoginStatusAdmin(admin.ModelAdmin):
	list_display = ('counterid','status')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Dishes,DishesAdmin)
admin.site.register(Orders,OrderssAdmin)
admin.site.register(BalanceAccount)
admin.site.register(CounterAccount)
admin.site.register(LoginStatus)

