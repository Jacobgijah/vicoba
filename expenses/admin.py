from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Loan, Category, Marital, House, Car


class LoanAdmin(admin.ModelAdmin):
    list_display = ("owner", "amount", "description", "category", "date")
    list_filter = ("description", "category", "date")
    # search_fields = ('description', 'category', 'date')
    list_per_page = 10


admin.site.register(Loan, LoanAdmin)
admin.site.register(Category)
admin.site.register(Marital)
admin.site.register(House)
admin.site.register(Car)
admin.site.unregister(Group)
