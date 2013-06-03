from django.contrib import admin
from expenses.models import *

class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('title','description','user','date','amount')
	date_hierarchy = 'date'

admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Refund)