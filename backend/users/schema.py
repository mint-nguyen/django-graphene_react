import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = get_user_model()(username=username, email=email)

        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Query(graphene.ObjectType):
    users = graphene.Field(UserType, id=graphene.String(required=True))
    me = graphene.Field(UserType)

    def resolve_users(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("User not logged in ")
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
