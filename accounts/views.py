from .serializers import SignUpSerializer
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(generics.GenericAPIView):

    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if User.objects.filter(username=data['username']).exists():
            # User with the same username already exists
            response = {"Message": "User with the same username already exists. Try another username!", "Status": "400 Bad request"}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            response = {"Message": "User created successfully!", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)

    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"Message": "Login successfull!", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"Message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
