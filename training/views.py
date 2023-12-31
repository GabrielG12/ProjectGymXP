from rest_framework import status, exceptions, filters
from rest_framework.permissions import IsAuthenticated
from .models import Training
from .serializers import TrainingCreateSerializer, TrainingUserListSerializer, TrainingDestroySerializer, \
    TrainingUserUpdateSerializer, TrainingUserRetrieveSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from accounts.models import User
from datetime import datetime, date


#TODO: VIEW FOR CREATING A TRAINING
class TrainingCreateView(CreateAPIView):
    serializer_class = TrainingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(username=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "Message": "Training created successfully!",
            "Status": "201 Created",
            "Data": serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)


#TODO: VIEW FOR LISTING ALL USER TRAININGS
class TrainingUserListView(ListAPIView):
    serializer_class = TrainingUserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        if self.request.user.is_authenticated and (self.request.user.username == username or self.request.user.is_staff):
            return Training.objects.filter(username=user)
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
                "Message": "You do not have any trainings yet!",
                "Status": "200 OK"
            }
            return Response(data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "Message": "These are the trainings for user {}!".format(self.kwargs['username']),
            "Status": "200 OK",
            "Data": serializer.data,
        }
        return Response(data, status=200)


#TODO: VIEW FOR RETRIEVING SPECIFIC USER EXERCISE
class TrainingUserRetrieveView(ListAPIView):
    serializer_class = TrainingUserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        date_str = self.kwargs['date']
        if self.request.user.is_authenticated and (self.request.user.username == username or self.request.user.is_staff):
            today = date.today()
            training_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if training_date <= today:
                return Training.objects.filter(username=user, date=training_date)
            else:
                raise exceptions.ValidationError({"Message": "You can only view trainings for the current day or past time!",
                                                  "Status": "400 Bad request"})
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
                "Message": "You did not do any trainings on this day!",
                "Status": "204 No content"
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "Status": "200 OK",
            "Message": "These are the trainings for user {} on {}!".format(self.kwargs['username'], self.kwargs['date']),
            "Data": serializer.data,
        }
        return Response(data, status=200)


#TODO: VIEW FOR DELETING SPECIFIC USER EXERCISE
class TrainingUserDestroyView(DestroyAPIView):
    serializer_class = TrainingDestroySerializer
    permission_classes = [IsAuthenticated]
    queryset = Training.objects.all()

    def get_object(self):
        username = self.kwargs['username']
        id = self.kwargs['id']
        if self.request.user.is_authenticated and (self.request.user.username == username or self.request.user.is_staff):
            try:
                return Training.objects.get(username__username=username, id=id)
            except Training.DoesNotExist:
                raise exceptions.NotFound("Training not found.")
        else:
            raise exceptions.PermissionDenied({"Message": "You are unauthorized to delete this exercise!", "Status": "403 Forbidden"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            "Message": "The exercise was deleted!",
            "Status": "204 No Content",
        }
        return Response(data, status=204)


#TODO: VIEW FOR DELETING SPECIFIC USER EXERCISE
class TrainingUserUpdateView(UpdateAPIView):
    serializer_class = TrainingUserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.kwargs['username']
        id = self.kwargs['id']
        if self.request.user.is_authenticated and (self.request.user.username == username or self.request.user.is_staff):
            try:
                return Training.objects.get(username__username=username, id=id)
            except Training.DoesNotExist:
                raise exceptions.NotFound("Exercise not found.")
        else:
            raise exceptions.PermissionDenied({"Message": "You are unauthorized to update this exercise!", "Status": "403 Forbidden"})

    def partial_update(self, request, *args, **kwargs):
        exercise = self.get_object()
        if not self.request.user.is_staff:
            update_data = request.data.copy()
            update_data.pop('username', None)
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
