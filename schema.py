import graphene
import json
from datetime import datetime
import uuid


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return 'https://cloudinary.com/{}/{}'.format(self.username, self.id)


class Query(graphene.ObjectType):
    hello = graphene.String()

    is_admin = graphene.Boolean()

    users = graphene.List(User)

    def resolve_hello(self, info):
        return "bye"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info):
        return [
            User(username='Mint'),
            User(username='Mint2'),
            User(username='Mint3'),
        ]


class CreateUser(graphene.Mutation):

    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        if (info.context.get('is_anonymous')):
            raise Exception('Not authenticated!')

        post = Post(title=title, content=content)

        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    
        mutation ($title: String, $content: String) {
            createPost(title: $title, content: $content) {
                post {
                    title
                    content
                }
            }
        }
                
        
    
    ''',
    variable_values={'title': 'Hello', 'content': 'Hi'},
    context={'is_anonymous': True}
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))
