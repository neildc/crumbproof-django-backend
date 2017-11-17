from rest_framework import serializers
from .recipe import RecipeSerializer, RecipeField
from .user import UserSerializer
from crumbproof.models import ActivityInProgress, Recipe

class ActivityInProgressSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    recipe = RecipeField(queryset=Recipe.objects.all())

    class Meta:
        model = ActivityInProgress
        fields = ( 'id'
                 , 'user'
                 , 'recipe'
                 , 'current_step'
                 , 'start_times'
                 , 'end_times'
                 )

    def create(self, validated_data):
        user =  self.context['request'].user

        # We should only have a single ActivityInProgress at any time
        if (ActivityInProgress.objects.filter(user=user).exists()):
            ActivityInProgress.objects.get(user=user).delete()

        new_activity = ActivityInProgress.objects.create(**validated_data)
        return new_activity
