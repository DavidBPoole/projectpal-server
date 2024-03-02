from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.decorators import action
from projectpalapi.models import Project, Task, Category, TaskCategory

class TaskView(ViewSet):
    """Task View"""
    
    def list(self, request):
        """Handle GET requests to get all tasks or filter by project."""
        try:
            project_id = request.query_params.get('project')
            if project_id:
                tasks = Task.objects.filter(project=project_id)
            else:
                tasks = Task.objects.all()
            keyword = request.query_params.get('keyword', None)
            
            if keyword:
                tasks = tasks.filter(
                    Q(name__icontains=keyword) |
                    Q(priority__icontains=keyword) |
                    Q(status__icontains=keyword)
                )

            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            categories = request.data["categories"]

            task = Task.objects.create(
                project=project,
                name=request.data["name"],
                description=request.data["description"],
                priority=request.data["priority"],
                status=request.data["status"],
            )
            
            for s_category in categories:
                category = Category.objects.get(id=s_category)
                TaskCategory.objects.create(
                    task = task,
                    category = category
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
            categories = request.data["categories"]
            task_categories = TaskCategory.objects.filter(task=task)
            
            def selected_categories(task_categories):
                return [task_category.category.id for task_category in task_categories]
            
            task.name = request.data["name"]
            task.description = request.data["description"]
            task.priority = request.data["priority"]
            task.status = request.data["status"]
            
            task.save()
            
            for s_category in categories:
                if s_category not in selected_categories(task_categories) :
                    category = Category.objects.get(id=s_category)
                    TaskCategory.objects.create(
                        task = task,
                        category = category
                    )

            for category_id in selected_categories(task_categories):
                if category_id not in categories :
                    category  = Category.objects.get(id=category_id)
                    task_category = TaskCategory.objects.get(task=task, category=category)
                    
                    task_category.delete()
                    
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
            print("Received data:", request.data)
            task = Task.objects.get(pk=pk)
            category_id = request.data.get('category')
            category = Category.objects.get(pk=category_id)

            if TaskCategory.objects.filter(task=task, category=category).exists():
                return Response({'message': 'Category already associated with the task'}, status=status.HTTP_400_BAD_REQUEST)

            task_category = TaskCategory.objects.create(task=task, category=category)
            
            serializer = TaskSerializer(task)
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
            print("Received data:", request.data)
            task = Task.objects.get(pk=pk)
            category_id = request.data.get('category')
            category = Category.objects.get(pk=category_id)

            task_category = TaskCategory.objects.get(task=task, category=category)
            
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
    
class TaskCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for BrewCategory"""
    id = serializers.ReadOnlyField(source='category.id')
    name = serializers.ReadOnlyField(source='category.name')

    class Meta:
      model = TaskCategory
      fields = ('id', 'name')
      
class TaskSerializer(serializers.ModelSerializer):
    """JSON serializer for tasks"""
    categories = TaskCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'priority', 'status', 'categories')
        depth = 1
