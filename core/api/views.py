from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from core.models import Task
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserRegistrationSerializer, UserListSerializer, TaskSerializer, UserLoginSerializer

class UserRegistrationView(APIView):

    @swagger_auto_schema(request_body = UserRegistrationSerializer)
    def post(self,request):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created succesfully"},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    @swagger_auto_schema(request_body = UserLoginSerializer)
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

class UserDetailView(APIView):

    #check if the user is exist
    def get_object(self,user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self,request,user_id):
        user = self.get_object(user_id)
        serializer = UserListSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)


class TaskListView(APIView):

    @swagger_auto_schema(responses = {200:TaskSerializer()})
    def get(self,request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class TaskDetailView(APIView):

    #check if the task is exist
    def get_object(self,task_id):
        try:
            return Task.objects.get(pk = task_id)
        except Task.DoesNotExist:
            raise Http404
    @swagger_auto_schema(responses = {200:TaskSerializer()})
    def get(self,request,task_id):
        task = self.get_object(task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status = status.HTTP_200_OK)

class UserTaskListView(APIView):

    user_id_param = openapi.Parameter(
        'user_id',
        openapi.IN_PATH,
        description = 'user id',
        type = openapi.TYPE_INTEGER
    )

    def get_object(self,user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            raise Http404
    @swagger_auto_schema(responses = {200:TaskSerializer()}, manual_parameters = [user_id_param])
    def get(self,request,user_id):
        user = self.get_object(user_id)
        user_tasks = user.tasks.all()
        serializer = TaskSerializer(user_tasks, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body = TaskSerializer,manual_parameters = [user_id_param])
    def post(self,request,user_id):
        user = self.get_object(user_id) #get the user by the user_id
        serializer = TaskSerializer(data = request.data, context = {'user':user}) #pass the user to the context
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserTaskDetailView(APIView):

    user_id_param = openapi.Parameter(
        'user_id',
        openapi.IN_PATH,
        description = 'user id',
        type = openapi.TYPE_INTEGER
    )

    task_id_param = openapi.Parameter(
        'task_id',
        openapi.IN_PATH,
        description = 'task id',
        type = openapi.TYPE_INTEGER
    )

    def get_object(self,user_id,task_id):
        try:
            user = User.objects.get(pk = user_id)
            return user.tasks.get(pk = task_id)
        except Task.DoesNotExist:
            raise Http404
    
    @swagger_auto_schema(responses = {200: TaskSerializer()}, manual_parameters = [user_id_param,task_id_param])
    def get(self,request,user_id,task_id):
        user_task = self.get_object(user_id,task_id)
        serializer = TaskSerializer(user_task)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body = TaskSerializer,responses = {200: TaskSerializer()}, manual_parameters = [user_id_param,task_id_param])
    def put(self,request,user_id,task_id):
        user_task = self.get_object(user_id,task_id)
        user = User.objects.get(pk = user_id)
        serializer = TaskSerializer(user_task, data = request.data, context = {"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,user_id,task_id):
        user_task = self.get_object(user_id,task_id)
        user_task.delete()
        return Response({'message':'task deleted successfully'},status = status.HTTP_200_OK)