from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from projectpalapi.models import TaskCategory


class TaskCategoryView(ViewSet):
    """TaskCategory View"""
    
    def list(self, request):
        """Handle GET requests to get all task categories."""
        try:
            task_categories = TaskCategory.objects.all()
            serializer = TaskCategorySerializer(task_categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        """Handle GET requests for a single task category."""
        try:
            task_category = TaskCategory.objects.get(pk=pk)
            serializer = TaskCategorySerializer(task_category)
            return Response(serializer.data)
        except TaskCategory.DoesNotExist:
            return Response({'message': 'TaskCategory not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """Handle POST requests to create a task-category relationship.
        Returns: Response -- JSON serialized task-category instance"""
        try:
            task_category = TaskCategory.objects.create(
                task=request.data["task"],
                category=request.data["category"]
            )
            serializer = TaskCategorySerializer(task_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    def destroy(self, request, pk):
        """Handle DELETE requests for a task category."""
        try:
            task_category = TaskCategory.objects.get(pk=pk)
            task_category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TaskCategory.DoesNotExist:
            return Response({'message': 'TaskCategory not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for task-categories"""
    # task = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = TaskCategory
        fields = ('id', 'task', 'category')
        # fields = ('id', 'category')
        
    # def get_task(self, obj):
    #     task = obj.task
    #     return {
    #         'id': task.id,
    #         'name': task.name,
    #         'description': task.description,
    #         'priority': task.priority,
    #         'status': task.status,
    #     }

    def get_category(self, obj):
        category = obj.category
        return {
            'id': category.id,
            'name': category.name,
        }
