"""drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from crumbproof import views
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'activities', views.ActivityViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^user/web_push_subscription/$', views.saveWebPushSubscription),
    url('^recipes/(?P<recipe>.+)/activities/$', views.RecipeActivities.as_view()),
    url(r'^activity_with_modified_recipe/$', views.CreateActivityWithModifiedRecipe.as_view()),
    url(r'^activity/live/$', views.LiveActivity.as_view()),
    url(r'^activity/live/start/$', views.LiveActivityStart.as_view()),
    url(r'^activity/live/next_step/$', views.liveActivityNextStep),
    url(r'^activity/live/start_timer/$', views.liveActivityStartTimer),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
