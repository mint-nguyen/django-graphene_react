import graphene
import json


class Query(graphene.ObjectType):
    hello = graphene.String()

    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "bye"

    def resolve_is_admin(self, info):
        return True


schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        isAdmin
    }
    '''
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult))
