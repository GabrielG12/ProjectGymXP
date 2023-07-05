from django.contrib import admin
from .models import Exercises

@admin.register(Exercises)
#TODO: TUKAJ POVEMO KAJ LAHKO ADMIN VIDI
class ExercisesAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'exercise_type', 'username')
    list_display = ('name', 'exercise_type', 'username')
    search_fields = ['name']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
