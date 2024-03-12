from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from projectpalapi.models import User

class UserView(ViewSet):
    """View for handling requests for users"""

    def retrieve(self, request, pk):
        """Handle GET request for a single user
        
        Returns -> Response -- JSON serialized user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all users
        
        Returns -> Response -- JSON serialized list of users"""
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk):
        """Handle PUT requests for a user
        Returns: Response -- Empty body with 204 status code"""
        try:
            user = User.objects.get(pk=pk)
            user.name = request.data["name"]
            user.bio = request.data["bio"]
            
            user.save()
            
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk):
        """Handle DELETE requests for a user
        Returns: Response -- Empty body with 204 status code"""
        try:
            user = User.objects.get(pk=pk)
            
            user.delete()
            
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for the User model"""
    class Meta:
        model = User
        fields = ('id', 'name', 'bio', 'uid')
