from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.db import *
from .serializers import TaskSerializer
import logging

logger = logging.getLogger(__name__)

class TaskListCreateAPIView(APIView):

    def get(self, request):
        tasks = get_all_tasks()
        return Response(tasks)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task_id = create_task(serializer.validated_data)
            return Response(
                {"id": task_id, "message": "Task created"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)


class TaskDetailAPIView(APIView):

    def get(self, request, pk):
        task = get_task(pk)
        if not task:
            return Response({"error": "Not found"}, status=404)
        return Response(task)

    def put(self, request, pk):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            update_task(pk, serializer.validated_data)
            return Response({"message": "Task updated"})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        delete_task(pk)
        return Response(status=204)