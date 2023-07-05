from . import views
from django.urls import path


urlpatterns = [

    path('create/', views.ExercisesCreateView.as_view(), name="exercise_create"),
    path('<str:username>/', views.ExercisesUserListView.as_view(), name="exercises_user"),
    path('delete/<str:username>/<str:name>/', views.ExercisesUserDestroyView.as_view(), name="exercise_delete"),
    path('<str:username>/<str:name>/', views.ExercisesUserUpdateView.as_view(), name="exercise_update"),

]
