from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from projectpalapi.models import User, Project, Collaborator
from projectpalapi.views.user import UserSerializer


class CollaboratorView(ViewSet):
    """Category View"""

    def list(self, request):
        """Handle GET requests to get all categories.
        Returns: Response -- JSON serialized list of categories"""
        try:
            collaborators = Collaborator.objects.all()
            serializer = CollaboratorSerializer(collaborators, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        """Handle GET requests for a single category.
        Returns: Response -- JSON serialized category"""

        try:
            collaborator = Collaborator.objects.get(pk=pk)
            serializer = CollaboratorSerializer(collaborator)
            return Response(serializer.data)
        except Collaborator.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        """Add a collaborator to a project."""
        try:
            project = Project.objects.get(pk=pk)
            user_id = request.data.get('user')
            user = User.objects.get(pk=user_id)

            # Check if the user is already a collaborator
            if Collaborator.objects.filter(project=project, user=user).exists():
                return Response({'message': 'User is already a collaborator on this project'}, status=status.HTTP_400_BAD_REQUEST)

            # Add the user as a collaborator
            collaborator = Collaborator.objects.create(project=project, user=user, is_owner=False)

            # Additional logic or response as needed

            return Response({'message': 'Collaborator added to project'}, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'])
    def leave_project(self, request, pk=None):
        """Allow a collaborator to leave a project."""
        try:
            user = User.objects.get(pk=request.data["userId"])
            project = Project.objects.get(pk=pk)

            # Check if the user is the project owner
            if project.user == user:
                return Response({'message': 'Project owner cannot leave the project'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user is a collaborator
            collaborator = Collaborator.objects.get(project=project, user=user)
            collaborator.delete()

            return Response({'message': 'User left the project'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Collaborator.DoesNotExist:
            return Response({'message': 'User is not a collaborator on this project'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'])
    def remove_collaborator(self, request, pk=None):
        """Remove a collaborator from the project (only for project owners)."""
        try:
            user = User.objects.get(pk=request.data["userId"])
            project = Project.objects.get(pk=pk)

            # Check if the user is the project owner
            if project.user != user:
                return Response({'message': 'Only project owner can remove collaborators'}, status=status.HTTP_403_FORBIDDEN)

            collaborator_id = request.data.get('collaborator')
            collaborator = Collaborator.objects.get(pk=collaborator_id, project=project)
            collaborator.delete()

            return Response({'message': 'Collaborator removed from the project'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Collaborator.DoesNotExist:
            return Response({'message': 'Collaborator not found on this project'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CollaboratorSerializer(serializers.ModelSerializer):
    """JSON serializer for collaborators"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Collaborator
        fields = ('id', 'user', 'project', 'is_owner')
        depth = 1
