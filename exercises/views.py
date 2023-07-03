from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from exercises.models import Exercises
from exercises.serializers import ExercisesSerializer
from rest_framework import generics, mixins
from rest_framework.response import Response

#TODO: VIEW FOR CREATING AN EXERCISE
class ExercisesCreateView(generics.GenericAPIView, mixins.CreateModelMixin):

    serializer_class = ExercisesSerializer
    queryset = Exercises.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(username=user)
        return super().perform_create(serializer)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#TODO: VIEW FOR RETRIEVING, UPDATING AND DELETING AN EXERCISE





