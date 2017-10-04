from django.contrib.auth.models import User, Group
from rest_framework import serializers
from crumbproof.models import Recipe, Activity, Ingredient, Instruction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.ReadOnlyField(source='user_id.username')

    class Meta:
        model = Recipe
        fields = ( 'url'
                 , 'name'
                 , 'prep_time'
                 , 'bake_time'
                 , 'oven_temperature'
                 , 'yield_count'
                 , 'yield_type'
                 , 'user_id'
                 , 'live'
                 , 'created'
                 , 'updated'
                 , 'deleted'
                 )
