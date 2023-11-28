from django.contrib import admin
from .models import Expenses, Category


# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("amount", "date", "desc", "owner", "category")
    search_fields = ("date", "desc", "category")
    list_per_page = 2


admin.site.register(Expenses, ExpenseAdmin)
admin.site.register(Category)
