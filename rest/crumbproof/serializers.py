from rest_framework import serializers
from crumbproof.models import Recipe, Activity, Ingredient, Instruction, User
from drf_extra_fields.fields import Base64ImageField


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    crumb_shot = Base64ImageField(required=False)
    recipe_name = serializers.ReadOnlyField(source='recipe.name')

    class Meta:
        model = Activity
        fields = ( 'id'
                 , 'name'
                 , 'user'
                 , 'recipe'
                 , 'recipe_name'
                 , 'started'
                 , 'created'
                 , 'completed'
                 , 'oven_start'
                 , 'oven_end'
                 , 'crumb_shot'
                 , 'notes'
                 )

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
                 , 'time_gap_to_next'
                 )


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
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
                 , 'user'
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
        new_recipe = Recipe.objects.create(**validated_data)
        for i in ingredients_data:
            Ingredient.objects.create(recipe=new_recipe, **i)

        for j in instructions_data:
            Instruction.objects.create(recipe=new_recipe, **j)

        return new_recipe

class UserSerializer(serializers.HyperlinkedModelSerializer):
    favourite_recipes = RecipeSerializer(many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'favourite_recipes')
