from django.contrib import admin
from .models import Training


@admin.register(Training)
#TODO: TUKAJ POVEMO KAJ LAHKO ADMIN VIDI
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('username', 'exercise', 'quantity_type',  'quantity', 'time_type', 'repetitions', 'date')
    search_fields = ['exercise', 'username']
    list_filter = ['username', 'exercise', 'quantity_type',  'quantity', 'time_type', 'repetitions', 'date']

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
