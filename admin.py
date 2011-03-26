from pycourt_login.models import *
from django.contrib import admin

class DishesAdmin(admin.ModelAdmin):
	list_display = ('dish_name','dish_price')
	search_fields = ('dish_name',)

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('is_counter',)
	search_fields = ('user.username',)
class OrderssAdmin(admin.ModelAdmin):
    list_display = ('order_id','student_id','counterid')
    search_fields = ('student_id',)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Dishes,DishesAdmin)
admin.site.register(Ordersss,OrderssAdmin)
admin.site.register(BalanceAccount)
admin.site.register(CounterAccount)
