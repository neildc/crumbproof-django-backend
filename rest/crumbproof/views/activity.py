from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions

from crumbproof.models import Activity
from crumbproof.serializers import ActivitySerializer
from crumbproof.serializers import ActivityWithModifiedRecipeSerializer

from crumbproof.permissions import IsOwnerOrReadOnly

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

class CreateActivityWithModifiedRecipe(generics.CreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivityWithModifiedRecipeSerializer
