import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Track, Like
from users.schema import UserType
from django.db.models import Q


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info, search=None):
        if search:
            return Track.objects.filter(Q(title__contains=search) | Q(description__contains=search))
        return Track.objects.all()

    def resolve_likes(self, info, **kwargs):
        return Like.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Log in required!')
        track = Track(title=title, description=description,
                      url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description, url):
        user = info.context.user

        track = Track.objects.get(id=track_id)

        if user != track.posted_by:
            raise Exception('Not permitted to update track!')
        track.title = title
        track.description = description
        track.url = url
        track.save()
        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user

        track = Track.objects.get(id=track_id)

        if user != track.posted_by:
            raise GraphQLError('Not permitted to delete track!')
        track.delete()
        return DeleteTrack(track_id=track_id)


class LikeTrack(graphene.Mutation):
    track = graphene.Field(TrackType)
    user = graphene.Field(UserType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Log in required!')

        track = Track.objects.get(id=track_id)

        if not track:
            raise Exception('Track not found!')

        Like.objects.create(user=user, track=track)

        return LikeTrack(user=user, track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    like_track = LikeTrack.Field()
