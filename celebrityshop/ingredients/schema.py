from django.db.models import Q
from graphene import relay, ObjectType, AbstractType

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from celebrityshop.ingredients.models import Category, Ingredient


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class Query(AbstractType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    def resolve_all_ingredients(self, info, request, *args, **kwargs):
        if request.user.username == 'test':
            return []
        return Ingredient.objects.filter(~Q(name='Chicken'))