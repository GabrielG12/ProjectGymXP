from . import views
from django.urls import path


urlpatterns = [

    path('create/', views.TrainingCreateView.as_view(), name="training_create"),
    path('<str:username>/', views.TrainingUserListView.as_view(), name="training_user"),
    path('<str:username>/<str:date>/', views.TrainingUserRetrieveView.as_view(), name="training_retrieve"),
    path('delete/<str:username>/<int:id>/', views.TrainingUserDestroyView.as_view(), name="training_delete"),
    path('<str:username>/<int:id>/', views.TrainingUserUpdateView.as_view(), name="training_update"),

]