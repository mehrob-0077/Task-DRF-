from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Category, Task
from .serialaizer import CategorySerializer, TaskSerializer


@api_view(['GET', 'POST'])
def category_list_view(request):
    if request.method == 'GET':
        return Response(CategorySerializer(Category.objects.filter(user=request.user), many=True).data)
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def category_create_view(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def category_detail_view(request, id):
    category = get_object_or_404(Category, id=id, user=request.user)
    return Response(CategorySerializer(category).data)


@api_view(['PUT', 'PATCH'])
def category_update_view(request, id):
    category = get_object_or_404(Category, id=id, user=request.user)
    serializer = CategorySerializer(category, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def category_delete_view(request, id):
    category = get_object_or_404(Category, id=id, user=request.user)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def task_list_view(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        return Response(TaskSerializer(tasks, many=True).data)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.validated_data['category']
        if category.user_id != request.user.id:
            return Response({'category': ['Категория ба шумо тааллуқ надорад.']}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def task_create_view(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.validated_data['category']
        if category.user_id != request.user.id:
            return Response({'category': ['Категория ба шумо тааллуқ надорад.']}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_detail_view(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    return Response(TaskSerializer(task).data)


@api_view(['PUT', 'PATCH'])
def task_update_view(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    serializer = TaskSerializer(task, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        category = serializer.validated_data.get('category', task.category)
        if category.user_id != request.user.id:
            return Response({'category': ['Категория ба шумо тааллуқ надорад.']}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def task_delete_view(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
