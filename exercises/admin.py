from django.contrib import admin
from .models import Exercises


@admin.register(Exercises)
#TODO: TUKAJ POVEMO KAJ LAHKO ADMIN VIDI
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'exercise_type')
    search_fields = ['name']
    list_filter = ['username', 'name', 'exercise_type']

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
