from . import views
from django.urls import path


urlpatterns = [

    path('create/', views.ExercisesCreateView.as_view(), name="exercise_create"),
    #path('<str:username>/<str:name>/', views.ExerciseDetailView.as_view, name="exercise_user"),

]