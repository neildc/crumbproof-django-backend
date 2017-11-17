from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status


from crumbproof.models import User
from crumbproof.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def saveWebPushSubscription(request):

    keys = ['endpoint', 'expirationTime' , 'keys']
    for k in keys:
        if k not in request.data:
            return Response('Invalid payload', status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    user.push_subscription = request.data;
    user.save()

    return Response({"status": { "success" : True }})
