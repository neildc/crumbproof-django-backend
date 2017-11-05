from rest_framework import serializers
from crumbproof.models import Recipe

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
