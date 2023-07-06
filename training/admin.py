from django.contrib import admin
from .models import Training


@admin.register(Training)
#TODO: TUKAJ POVEMO KAJ LAHKO ADMIN VIDI
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'quantity_type', 'username', 'quantity', 'date')
    search_fields = ['exercise', 'username']

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
