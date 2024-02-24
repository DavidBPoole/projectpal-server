from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from projectpalapi.models import Project, Task, Category
from .task_category import TaskCategory, TaskCategorySerializer

class TaskView(ViewSet):
    """Task View"""

    # def list(self, request):
    #     """Handle GET requests to get all tasks.
    #     Returns: Response -- JSON serialized list of tasks"""
    #     try:
    #         tasks = Task.objects.all()
    #         serializer = TaskSerializer(tasks, many=True)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        """Handle GET requests to get all tasks or filter by project."""
        try:
            project_id = request.query_params.get('project')
            if project_id:
                tasks = Task.objects.filter(project=project_id)
            else:
                tasks = Task.objects.all()

            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def list(self, request):
    #     """Handle GET requests to get all tasks.
    #     Returns: Response -- JSON serialized list of tasks"""
    #     try:
    #         project_id = self.request.query_params.get('project')
    #         tasks = Task.objects.filter(project=project_id)
    #         serializer = TaskSerializer(tasks, many=True)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        """Handle GET requests for single task.
        Returns: Response -- JSON serialized task"""

        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized task instance"""
        print("Request Data:", request.data)
        try:
            project = Project.objects.get(pk=request.data["project"])

            task = Task.objects.create(
                project=project,
                name=request.data["name"],
                description=request.data["description"],
                priority=request.data["priority"],
                status=request.data["status"],
            )
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a task
        Returns: Response -- Empty body with 204 status code"""

        try:
            task = Task.objects.get(pk=pk)
            task.name = request.data["name"]
            task.description = request.data["description"]
            task.priority = request.data["priority"]
            task.status = request.data["status"]

            task.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a task
        Returns: Response -- Empty body with 204 status code"""

        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'])
    def add_task_category(self, request, pk=None):
        """Add a category to a task."""
        try:
            task = Task.objects.get(pk=pk)
            category_id = request.data.get('category')
            category = Category.objects.get(pk=category_id)

            # Check if the category is already associated with the task
            if TaskCategory.objects.filter(task=task, category=category).exists():
                return Response({'message': 'Category already associated with the task'}, status=status.HTTP_400_BAD_REQUEST)

            # Create TaskCategory entry to associate the category with the task
            task_category = TaskCategory.objects.create(task=task, category=category)
            
            # You can return the serialized task or task_category if needed
            serializer = TaskSerializer(task)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message': 'Category added to task'}, status=status.HTTP_201_CREATED)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['delete'])
    def remove_task_category(self, request, pk=None):
        """Remove a category from a task."""
        try:
            task = Task.objects.get(pk=pk)
            category_id = request.data.get('category')
            category = Category.objects.get(pk=category_id)

            # Check if the category is associated with the task
            task_category = TaskCategory.objects.get(task=task, category=category)
            
            # Delete TaskCategory entry to disassociate the category from the task
            task_category.delete()

            return Response({'message': 'Category removed from task'}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except TaskCategory.DoesNotExist:
            return Response({'message': 'Category is not associated with the task'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

          
# original working serializer:
# class TaskSerializer(serializers.ModelSerializer):
#     """JSON serializer for tasks"""
#     categories = TaskCategorySerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Task
#         fields = ('id', 'name', 'description', 'priority', 'status', 'categories')
#         depth = 2

# updated serializer to display only added category names on a task:
class TaskSerializer(serializers.ModelSerializer):
    # category_ids = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'priority', 'status', 'categories')

    # def get_category_ids(self, obj):
    #     return [category.category_id for category in obj.categories.all()]

    def get_categories(self, obj):
        return [category.category.name for category in obj.categories.all()]
