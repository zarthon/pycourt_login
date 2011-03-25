from pycourt_login.models import *
from django.contrib import admin

class DishesAdmin(admin.ModelAdmin):
	list_display = ('dish_name','dish_price')
	search_fields = ('dish_name',)

admin.site.register(UserProfile)
admin.site.register(Dishes,DishesAdmin)
admin.site.register(Orders)
admin.site.register(BalanceAccount)
admin.site.register(CounterAccount)
