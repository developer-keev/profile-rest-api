from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import HelloSerializers, UserProfileSerializer, ProfileFeedItemSerializer
from .models import UserProfile, ProfileFeedItem
from profile_api import permission

from rest_framework.permissions import IsAuthenticated

class HelloAPIView(APIView):
    """Test API View"""
    serializer_class = HelloSerializers

    def get(self, request, format=None):
        """returm list of api feature"""
        an_apiview = [
        'Uses HTTP methods as functions (get, post, put, patch, delete)',
        'is similarto traditional django views',
        'Gives you the most control over you application logic',
        'Is mapped manually to urls'
        ]
        return Response({'messages': "hello", 'an_apiview':an_apiview})

    def post(self, request, *args, **kwargs):
        """create a hello message with a name"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello {name}'
            return Response({'message':message})
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test View set"""
    serializer_class = HelloSerializers

    def list(self, request):
        a_viewset = [
        'Uses actions (list, create, retrive, update, partial update)',
        'automatically map to URLs using routers',
        'Provide more functionality with less code',
        ]
        return Response({'message':"Hello", 'a_viewset':a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginAPIView(ObtainAuthToken):
    """handle creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed Item"""
    authentication_classes=(TokenAuthentication,)
    serializer_class=ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    permission_classes = (
        permission.UpdateOwnStatus,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)
