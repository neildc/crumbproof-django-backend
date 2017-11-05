from rest_framework import serializers
from .recipe import RecipeSerializer
from .user import UserSerializer
from crumbproof.models import Activity, Recipe
from drf_extra_fields.fields import Base64ImageField
import uuid

class RecipeField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        pk = super(RecipeField, self).to_representation(value)
        try:
            item = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(item)
            return serializer.data
        except Recipe.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([(item.id, str(item)) for item in queryset])


#
class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    crumb_shot = Base64ImageField(required=False)
    recipe = RecipeField(required=False, queryset=Recipe.objects.all())

    class Meta:
        model = Activity
        fields = ( 'id'
                 , 'name'
                 , 'user'
                 , 'recipe'
                 , 'started'
                 , 'created'
                 , 'completed'
                 , 'oven_start'
                 , 'oven_end'
                 , 'crumb_shot'
                 , 'notes'
                 )


class ActivityWithModifiedRecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    crumb_shot = Base64ImageField(required=False)
    recipe = RecipeSerializer()


    class Meta:
        model = Activity
        fields = ( 'id'
                 , 'name'
                 , 'user'
                 , 'recipe'
                 , 'started'
                 , 'created'
                 , 'completed'
                 , 'oven_start'
                 , 'oven_end'
                 , 'crumb_shot'
                 , 'notes'
                 )

    def validate_recipe(self, value):
            return value


    def create(self, validated_data):
        user =  self.context['request'].user
        recipe_data = validated_data.pop('recipe')

        for k in ['instructions', 'ingredients']:
            diff = recipe_data['diff'][k]
            if diff and diff['added']:
                for obj in recipe_data['data'][k]:
                    # Only newly added objects won't have a UUID
                    if 'id' not in obj:
                        uuid_str = str(uuid.uuid4())
                        # The object added in the diff and data object
                        # should have the same UUID
                        for added in diff['added']:
                            if obj == added:
                                added['id'] = uuid_str
                                obj['id'] = uuid_str


        new_recipe = Recipe.objects.create(user=user,**recipe_data)
        new_activity = Activity.objects.create(recipe=new_recipe,**validated_data)
        return new_activity
