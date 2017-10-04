from django.shortcuts import render

from django.contrib.auth.models import User, Group
from crumbproof.models import Recipe, Activity, Ingredient, Instruction
from rest_framework import viewsets
from crumbproof.serializers import UserSerializer, GroupSerializer, RecipeSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all().order_by('name')
    serializer_class = RecipeSerializer
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

