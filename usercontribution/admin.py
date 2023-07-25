from django.contrib import admin
from .models import UserContribution, Source
   
# Register your models here.
@admin.register(UserContribution)
class UserContributionAdmin(admin.ModelAdmin):
    list_display = ("owner", "amount", "description", "source", "date")

admin.site.register(Source)