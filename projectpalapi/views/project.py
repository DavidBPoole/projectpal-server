from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from projectpalapi.models import Project, User, Collaborator
from .task import TaskSerializer
from .collaborator import CollaboratorSerializer

class ProjectView(ViewSet):
    """Project View"""
    
    def list(self, request):
        """Handle GET requests to get all projects for a specific user."""
        try:
            user_id = request.query_params.get('userId', None)

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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
    collaborators = CollaboratorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ('id', 'user', 'name', 'description', 'due_date', 'status', 'tasks', 'collaborators')
        depth = 2
