from rest_framework import serializers
from .recipe import RecipeSerializer
from crumbproof.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    favourite_recipes = RecipeSerializer(many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'favourite_recipes')
