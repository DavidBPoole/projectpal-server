from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
from projectpalapi.models import Project, User
from .task import TaskSerializer

class ProjectView(ViewSet):
    """Project View"""
    # queryset = Project.objects.all()
    
    # This function returns ALL projects regardless of user that created it.
    # def list(self, request):
    #     """Handle GET requests to get all projects.
    #     Returns: Response -- JSON serialized list of projects"""
    #     try:
    #         projects = Project.objects.all()
    #         serializer = ProjectSerializer(projects, many=True)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # def list(self, request):
    #     """Handle GET requests to get all projects.
    #     Returns: Response -- JSON serialized list of projects"""
    #     try:
    #         user_id = self.request.query_params.get('user')
    #         user = User.objects.get(pk=user_id)
    #         projects = Project.objects.filter(user=user)
    #         serializer = ProjectSerializer(projects, many=True)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # def list(self, request, *args, **kwargs):
    #     user_id = request.query_params.get('user')
    #     user = User.objects.get(pk=user_id)
    #     projects = Project.objects.filter(user=user)
    #     serializer = ProjectSerializer(projects, many=True)
    #     return Response(serializer.data)

        
    # def list(self, request):
    #     try:
    #         user_id = request.query_params.get('userId', None)

    #         if user_id is not None:
    #             user = User.objects.get(id = user_id)
    #             projects = Project.objects.filter(user_id=user)
    #         else:
    #             projects = Project.objects.all()

    #         serializer = ProjectSerializer(projects, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    # def list(self, request):
    #     """Handle GET requests to get user authenticated projects.
    #     Returns: Response -- JSON serialized list of projects"""
    #     user_id = self.request.query_params.get('user')
    #     print(f"Received user ID: {user_id}")
    #     try:
    #         # Ensure user_id is an integer
    #         user_id = int(user_id)

    #         user = User.objects.get(pk=user_id)
    #         projects = Project.objects.filter(user=user)
    #         serializer = ProjectSerializer(projects, many=True)
    #         return Response(serializer.data)
    #     except User.DoesNotExist:
    #         return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response({'message': 'Invalid user ID format'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # @action(detail=False, methods=['get'])
    # def user_projects(self, request):
    #     """
    #     Retrieve projects for the authenticated user.
    #     """
    #     # Assuming you have a user associated with the request
    #     user = request.user

    #     if user.is_authenticated:
    #         projects = Project.objects.filter(user=user)
    #         serializer = ProjectSerializer(projects, many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    # def list(self, request, *args, **kwargs):
    #     user_id = request.query_params.get('uid')
    #     try:
    #         user = User.objects.get(pk=user_id)
    #         projects = Project.objects.filter(user=user)
    #         serializer = ProjectSerializer(projects, many=True)
    #         return Response(serializer.data)
    #     except User.DoesNotExist:
    #         return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response({'message': 'Invalid user ID format'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        """Handle GET requests to get all projects for a specific user."""
        try:
            # Gets user ID from the request
            user_id = request.query_params.get('userId', None)

            # Check if user with the given ID exists
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Filters projects based on the user's ID
            projects = Project.objects.filter(user__id=user_id)

            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single project.
        Returns: Response -- JSON serialized project"""
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized project instance"""
        try:
            user = User.objects.get(pk=request.data["userId"])
            project = Project.objects.create(
                user=user,
                name=request.data["name"],
                description=request.data["description"],
                due_date=request.data["due_date"],
                status=request.data["status"],
            )
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # @action(detail=False, methods=['get'])
    # def create_project(self, request):
    #     user_id = self.request.query_params.get('user')
    #     user = User.objects.get(pk=user_id)
    #     projects = Project.objects.filter(user=user)
    #     serializer = ProjectSerializer(projects, many=True)
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     user_id = self.request.data.get('user')
    #     user = User.objects.get(pk=user_id)
    #     serializer.save(user=user)
        
    def update(self, request, pk):
        """Handle PUT requests for a project
        Returns: Response -- Empty body with 204 status code"""
        try:
            project = Project.objects.get(pk=pk)
            project.name = request.data["name"]
            project.description = request.data["description"]
            project.due_date = request.data["due_date"]
            project.status = request.data["status"]
            project.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk):
        """Handle DELETE requests for a project
        Returns: Response -- Empty body with 204 status code"""
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProjectSerializer(serializers.ModelSerializer):
  """JSON serializer for projects"""
  
  tasks = TaskSerializer(many=True, read_only=True)
  
  class Meta:
    model = Project
    fields = ('id', 'user', 'name', 'description', 'due_date', 'status', 'tasks')
    depth = 1
