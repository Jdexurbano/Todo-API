from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserListSerializer

class UserRegistrationView(APIView):
    
    def post(self,request):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created succesfully"},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username = username, password = password)
        if user:
            return Response({"message":"succesfully login"}, status = status.HTTP_200_OK)
        return Response({"error":"invalid credentials"}, status = status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    
    def get(self,request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)