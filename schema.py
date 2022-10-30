import graphene
import json


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "bye"


schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        hello
    }
    '''
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult))
