from django.shortcuts import render
from User.models import User
from User.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action

class UserListAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    # @action
    # def blockuser(self):
    #