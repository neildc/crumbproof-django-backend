from django.shortcuts import render

from crumbproof.models import Recipe, Activity, User
from rest_framework import viewsets, generics
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


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Activitys to be viewed or edited.
    """
    queryset = Activity.objects.all().order_by('-created')
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

    @detail_route(methods=['get'])
    def activity_history(self, request, pk=None):
        recipe = self.get_object()
        history = recipe.activities.all().order_by('-created') #Most recent first
        serializer = ActivitySerializer(history, many=True)
        return Response(serializer.data)

class RecipeActivities(generics.ListAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        recipe = self.kwargs['recipe']
        return Activity.objects.filter(recipe=recipe).order_by('-created')

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        response.data["recipe"] = self.kwargs['recipe']
        return response
