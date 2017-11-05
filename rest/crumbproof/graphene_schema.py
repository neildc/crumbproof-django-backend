from .models import User as UserModel
from .models import Recipe as RecipeModel
from .models import Activity as ActivityModel

from graphene_django import DjangoObjectType
import graphene

class User(DjangoObjectType):
    class Meta:
        model = UserModel

class Activity(DjangoObjectType):
    class Meta:
        model = ActivityModel

class Recipe(DjangoObjectType):
    class Meta:
        model = RecipeModel

class Query(graphene.ObjectType):
    users = graphene.List(User)
    recipes = graphene.List(Recipe)

    recipe = graphene.Field(Recipe,
                              id=graphene.Int())
    activities = graphene.List(Activity)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()

    @graphene.resolve_only_args
    def resolve_activities(self):
        return ActivityModel.objects.all()

    @graphene.resolve_only_args
    def resolve_recipes(self):
        return RecipeModel.objects.all()

    def resolve_recipe(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return RecipeModel.objects.get(pk=id)

        return None

schema = graphene.Schema(query=Query)
