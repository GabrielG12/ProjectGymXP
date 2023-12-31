from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Exercises
from exercises.serializers import ExercisesCreateSerializer, ExercisesUserListSerializer, \
    ExercisesDestroySerializer, ExercisesUpdateSerializer
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from django.http import Http404


#TODO: VIEW FOR CREATING AN EXERCISE
class ExercisesCreateView(CreateAPIView):

    serializer_class = ExercisesCreateSerializer
    queryset = Exercises.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        name = serializer.validated_data['name']
        existing_exercise = Exercises.objects.filter(username=user, name=name).exists()
        if existing_exercise:
            raise serializers.ValidationError({"Message": "Exercise with this name already exists!", "Status": "400 Bad request"})
        serializer.save(username=user)
        return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "Message": "Exercise created successfully!",
            "Status": "201 Created",
            "Data": serializer.data
        }
        return Response(data)


#TODO: VIEW FOR LISTING ALL USER EXERCISES

class ExercisesUserListView(ListAPIView):
    serializer_class = ExercisesUserListSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    #Pogledamo če je uporabnik avtoriziran za dostop do objekta!
    def get_queryset(self):
        username = self.kwargs['username']
        if self.request.user.is_authenticated and (self.request.user.username == username or self.request.user.is_staff):
            return Exercises.objects.filter(username=username)
        else:
            raise exceptions.PermissionDenied

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except exceptions.PermissionDenied:
            return Response(
                {"Message": "You are unauthorized for accessing this object!",
                 "Status": "403 Forbidden"},
                status=403
            )
        if not queryset.exists():
            data = {
                "Message": "You do not have any exercises yet!",
                "Status": "200 OK"
            }
            return Response(data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "Message": "These are the exercises for user {}!".format(self.kwargs['username']),
            "Status": "200 OK",
            "Data": serializer.data,
        }
        return Response(data, status=200)


#TODO: VIEW FOR DESTROYING SPECIFIC USER EXERCISE

class ExercisesUserDestroyView(DestroyAPIView):
    serializer_class = ExercisesDestroySerializer
    permission_classes = [IsAuthenticated | IsAdminUser]
    queryset = Exercises.objects.all()

    # Pogledamo če je uporabnik avtoriziran za dostop do objekta!
    def get_queryset(self):
        username = self.kwargs['username']
        name = self.kwargs['name']
        if self.request.user.is_authenticated and (self.request.user.username == username or self.request.user.is_staff):
            return Exercises.objects.filter(username=username, name=name)
        else:
            raise exceptions.PermissionDenied

    def destroy(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except exceptions.PermissionDenied:
            return Response(
                {"Message": "You are unauthorized for accessing this object!",
                 "Status": "403 Forbidden"},
                status=403
            )
        instance = queryset
        self.perform_destroy(instance)
        data = {
            "Message": "The exercise was deleted!",
            "Status": "204 No Content"
        }
        return Response(data)


#TODO: VIEW FOR UPDATING SPECIFIC USER EXERCISE


class ExercisesUserRetrieveUpdateView(UpdateAPIView):
    serializer_class = ExercisesUpdateSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    def get_object(self):
        username = self.kwargs['username']
        name = self.kwargs['name']
        try:
            exercise = Exercises.objects.get(username=username, name=name)
        except Exercises.DoesNotExist:
            raise Http404("Exercise not found!")

        if (
            not self.request.user.is_authenticated
            or (self.request.user.username != username and not self.request.user.is_staff)
        ):
            raise PermissionDenied({"Message": "You are unauthorized to update this exercise!", "Status": "403 Forbidden"})

        return exercise

    def partial_update(self, request, *args, **kwargs):
        exercise = self.get_object()
        if not self.request.user.is_staff:
            # If the user is not an admin, exclude the 'username' field from the update
            update_data = request.data.copy()
            update_data.pop('username', None)  # Remove the 'username' field from the update data
            serializer = self.get_serializer(exercise, data=update_data, partial=True)
        else:
            serializer = self.get_serializer(exercise, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "Message": "The exercise was updated!",
            "Status": "200 OK",
            "Data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

