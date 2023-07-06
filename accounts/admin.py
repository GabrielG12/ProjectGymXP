from django.contrib import admin
from .models import User


@admin.register(User)
#TODO: TUKAJ POVEMO KAJ LAHKO ADMIN VIDI
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['username']