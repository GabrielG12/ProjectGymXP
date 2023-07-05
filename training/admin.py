from django.contrib import admin
from .models import Training

@admin.register(Training)
#TODO: TUKAJ POVEMO KAJ LAHKO ADMIN VIDI
class ExercisesAdmin(admin.ModelAdmin):
    readonly_fields = ('exercise', 'type', 'username', 'type', 'quantity', 'date')
    list_display = ('exercise', 'type', 'username', 'type', 'quantity', 'date')
    search_fields = ['exercise', 'username']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
