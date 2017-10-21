from django.shortcuts import render

from crumbproof.models import Recipe, Activity, Ingredient, Instruction, User
from rest_framework import viewsets
from crumbproof.serializers import *
from rest_framework import permissions
from crumbproof.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import detail_route
from rest_framework import status

from rest_framework.response import Response



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


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Activitys to be viewed or edited.
    """
    queryset = Activity.objects.all().order_by('created')
    serializer_class = ActivitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all().order_by('name')
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['post'])
    def favourite(self, request, pk=None):
        recipe = self.get_object()
        if request.auth:
            request.user.favourite_recipes.add(recipe)
            request.user.save()
            return Response({'status': 'favourite added'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def unfavourite(self, request, pk=None):
        recipe = self.get_object()
        if request.auth:
            request.user.favourite_recipes.remove(recipe)
            request.user.save()
            return Response({'status': 'favourite removed'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_401_UNAUTHORIZED)
