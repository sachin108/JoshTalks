from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.shortcuts import render
from django.http import JsonResponse

def task_list(request):
    tasks = Task.objects.all().values('id', 'name', 'description', 'task_type', 'completed_at')
    task_list = list(tasks)  
    return JsonResponse({'tasks': task_list})

def user_list(request):
    users = User.objects.all().values('id', 'username', 'email')
    user_list = list(users)  
    return JsonResponse({'users': user_list})

def home(request):
    project_name = "Task Management App"
    return render(request, 'home.html', {'project_name': project_name})

class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            user_serializer = UserSerializer(user) 
            return Response({'message': 'User created successfully', 'user': user_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({'message': 'Task created successfully', 'task': TaskSerializer(task).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignTaskView(APIView):
    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        user_ids = request.data.get('user_ids', [])
        users = User.objects.filter(id__in=user_ids)

        if users.exists():
            task.users.set(users)
            return Response({'message': 'Task assigned successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'No valid users found'}, status=status.HTTP_400_BAD_REQUEST)

class UserTasksView(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(users__id=user_id)
