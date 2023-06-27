
# Create your views here.
import datetime
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

User = get_user_model()

factory = APIRequestFactory()
request = factory.get('/')


serializer_context = {
    'request': Request(request),
}

"""
API endpoint that returns the current user.
"""


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    permission_classes = [permissions.IsAuthenticated]


"""
API endpoint that returns list of users based on the user type.
"""


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    serializer_class = UserSerializer
    queryset = User.objects

    def get_queryset(self):
        return User.objects.filter().exclude(boarded_by=None).order_by('-date_joined').select_related('boarded_by')

    permission_classes = [permissions.IsAuthenticated]


"""
API endpoint that fills the onboard user information.
"""
