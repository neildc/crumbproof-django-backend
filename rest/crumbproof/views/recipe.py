from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.decorators import detail_route

from crumbproof.models import Recipe, Activity, User
from crumbproof.serializers import RecipeSerializer, ActivitySerializer
from crumbproof.permissions import IsOwnerOrReadOnly

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


class RecipeActivities(generics.ListAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        recipe = self.kwargs['recipe']
        return Activity.objects.filter(recipe=recipe).order_by('-created')

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        response.data["recipe"] = self.kwargs['recipe']
        return response
