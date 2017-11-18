from rest_framework import serializers
from crumbproof.models import Recipe
import uuid

class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Recipe
        fields = ( 'id'
                 , 'user'
                 , 'data'
                 , 'diff'
                 , 'base_recipe'
                 , 'parent'
                 , 'created'
                 )

    def addUUIDs(self, array):
        for obj in array:
            if 'id' not in obj:
                obj['id'] = str(uuid.uuid4())

    def create(self, validated_data):
        recipe_data = validated_data.pop('data')
        recipe_diff = validated_data.pop('diff')

        self.addUUIDs(recipe_data['instructions'])
        self.addUUIDs(recipe_data['ingredients'])

        new_recipe = Recipe.objects.create(data=recipe_data, diff=recipe_diff,**validated_data)
        return new_recipe


# Used to have a field which we can write a primary key to the
# POST when creating, but in the GET it serializes the entire object
# for the same PK
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
