from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db import transaction
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
        
# MY ORIGINAL CREATE FUNCTION ****************
    # def create(self, request):
    #     """Handle POST operations
    #     Returns Response -- JSON serialized task instance"""
    #     print("Request Data:", request.data)
    #     try:
    #         project = Project.objects.get(pk=request.data["project"])

    #         task = Task.objects.create(
    #             project=project,
    #             name=request.data["name"],
    #             description=request.data["description"],
    #             priority=request.data["priority"],
    #             status=request.data["status"],
    #         )
    #         serializer = TaskSerializer(task)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Project.DoesNotExist:
    #         return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Create function expects to have "categories" in the post body, if not, it fails unlike above - may leave it empty string and still runs.
    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized task instance"""
        print("Request Data:", request.data)
        try:
            project = Project.objects.get(pk=request.data["project"])
            categories = request.data["categories"] # Must include "categories" in the post body or fails - may leave as empty string ***

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

    # MY ORIGINAL UPDATE FUNCTION ******************
    # def update(self, request, pk):
    #     """Handle PUT requests for a task
    #     Returns: Response -- Empty body with 204 status code"""

    #     try:
    #         task = Task.objects.get(pk=pk)
            
    #         task.name = request.data["name"]
    #         task.description = request.data["description"]
    #         task.priority = request.data["priority"]
    #         task.status = request.data["status"]

    #         task.save()

    #         return Response(None, status=status.HTTP_204_NO_CONTENT)
    #     except Task.DoesNotExist:
    #         return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Original updated UPDATE function without transaction to stop duped categories Best version for goal ********
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

# Confirmed working in postman and will not allow duplicate categories to be associated ************
    # def update(self, request, pk):
    #     """Handle PUT requests for a task
    #     Returns: Response -- Empty body with 204 status code"""

    #     try:
    #         with transaction.atomic():
    #             task = Task.objects.get(pk=pk)
    #             categories = request.data.get("categories", [])
    #             task_categories = TaskCategory.objects.filter(task=task)

    #             existing_category_ids = set(task_category.category.id for task_category in task_categories)

    #             task.name = request.data.get("name", task.name)
    #             task.description = request.data.get("description", task.description)
    #             task.priority = request.data.get("priority", task.priority)
    #             task.status = request.data.get("status", task.status)
    #             task.save()

    #             new_categories = [Category.objects.get(id=s_category) for s_category in categories
    #                             if s_category not in existing_category_ids]

    #             for new_category in new_categories:
    #                 if new_category.id not in existing_category_ids:
    #                     TaskCategory.objects.create(task=task, category=new_category)
    #                     existing_category_ids.add(new_category.id)

    #             return Response(None, status=status.HTTP_204_NO_CONTENT)
    #     except Task.DoesNotExist:
    #         return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Category.DoesNotExist:
    #         return Response({'message': 'One or more categories not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        
    # MY ORIGINAL ACTION ADD
    @action(detail=True, methods=['post'])
    def add_task_category(self, request, pk=None):
        """Add a category to a task."""
        try:
            print("Received data:", request.data)
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
    
    # @action(methods=['post'], detail=True)
    # def add_task_category(self, request, pk):
    #     """Associates the many to many relationship between task and category"""

    #     task = Task.objects.get(pk=pk)
    #     category_id = request.data.get('category')
    #     try:
    #         category = Category.objects.get(id=category_id)
    #         TaskCategory.objects.get(task=task, category=category)
    #         return Response({'message': 'Task already associated with this category'})
    #     except TaskCategory.DoesNotExist:
    #         TaskCategory.objects.create(task=task, category=category)
    #         serializer = TaskSerializer(task)
    #         return Response({'message': 'Category added to task'}, status=status.HTTP_201_CREATED)
    #     except Task.DoesNotExist:
    #         return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Category.DoesNotExist:
    #         return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # MY ORIGINAL ACTION DELETE:
    @action(detail=True, methods=['delete'])
    def remove_task_category(self, request, pk=None):
        """Remove a category from a task."""
        try:
            print("Received data:", request.data)
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
    
    # @action(methods=['delete'], detail=True)
    # def remove_task_category(self, request, pk):
    #     """Disassociates the many to many relationship between task and category"""
    #     try:
    #         task_category = TaskCategory.objects.get(pk=pk)
    #         task_category.delete()
    #         return Response({'message': 'Category removed from task'}, status=status.HTTP_204_NO_CONTENT)
    #     except Task.DoesNotExist:
    #         return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Category.DoesNotExist:
    #         return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except TaskCategory.DoesNotExist:
    #         return Response({'message': 'Category is not associated with the task'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# original working serializer (displays "object Object"):
# class TaskSerializer(serializers.ModelSerializer):
#     """JSON serializer for tasks"""
#     categories = TaskCategorySerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Task
#         fields = ('id', 'name', 'description', 'priority', 'status', 'categories')
#         depth = 2

# updated serializer to display only added category names on a task (avoids displaying "object Object" on cards):
class TaskSerializer(serializers.ModelSerializer):
    # category_ids = serializers.SerializerMethodField() # displays category id's in test results - comment out to hide
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'priority', 'status', 'categories')

    # def get_category_ids(self, obj): # displays category id in test results - comment out to hide
    #     return [category.category_id for category in obj.categories.all()]

    def get_categories(self, obj):
        return [category.category.name for category in obj.categories.all()]
