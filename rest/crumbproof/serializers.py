from django.contrib.auth.models import User, Group
from rest_framework import serializers
from crumbproof.models import Recipe, Activity, Ingredient, Instruction
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ( 'name'
                 , 'id'
                 , 'unit'
                 , 'quantity'
                 )

class InstructionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instruction
        fields = ( 'step_number'
                 , 'content'
                 )

class RecipeSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user_id.username')
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ( 'name'
                 , 'id'
                 , 'prep_time'
                 , 'bake_time'
                 , 'oven_temperature'
                 , 'yield_count'
                 , 'yield_type'
                 , 'user_id'
                 , 'live'
                 , 'ingredients'
                 , 'instructions'
                 )

    def validate_ingredients(self, value):
            if not value:
                raise serializers.ValidationError("Must provide at least 1 ingredient")
            return value

    def validate_instructions(self, value):
            if not value:
                raise serializers.ValidationError("Must provide at least 1 instruction")
            return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instructions_data = validated_data.pop('instructions')
        recipe = Recipe.objects.create(**validated_data)
        for i in ingredients_data:
            Ingredient.objects.create(recipe_id=recipe, **i)

        for j in instructions_data:
            Instruction.objects.create(recipe_id=recipe, **j)

        return recipe
