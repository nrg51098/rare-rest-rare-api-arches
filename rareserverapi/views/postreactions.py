from rareserverapi.models import Post, PostReactions, Reaction
from rareserverapi.serializers import PostReactionSerializer
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action


class PostReactionViewSet(ViewSet):
    # Data that should be received in a request:
    # {
    #     "post_id": 0,  -> id of post
    #     "reaction_id": 0 -> id of reaction
    # }
    #
    # Note: The 'user_id' is pull from the request details

    # Because we aren't deleting a specific postreaction record directly, we need to use our own function so we don't have to pass in a pk via the path since deletion data will be coming in via the body.
    #
    # SEE: https://stackoverflow.com/a/51637525/13029557 for more details
    @action(methods=['DELETE'], detail=False)
    def delete(self, request):
        user_id = request.user.id
        try:
            post = Post.objects.get(pk=request.data["post_id"])
            postreaction = PostReactions.objects.get(
                user_id=user_id, reaction_id=request.data["reaction_id"])

            post.reactions.remove(postreaction)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        # Python provides the user data that matches the token used in the request. We use this to grab the id for that user's record
        user_id = request.user.id

        # Need to make sure the data that was provided was valid, otherwise, handle gracefully (i.e. make sure the post, user, and reaction all exist before we attempt to use them)
        try:
            post = Post.objects.get(pk=request.data["post_id"])
            user = User.objects.get(pk=user_id)
            reaction = Reaction.objects.get(pk=request.data["reaction_id"])

        except Exception as ex:
            return HttpResponseServerError(ex)

        try:
            # If the specific reaction and user combination already exists (i.e. that user has used that reaction before), grab that combo
            postreaction = PostReactions.objects.get(
                user_id=user_id, reaction_id=request.data["reaction_id"])

            # if postreaction does exist, we then attach that reaction to the post, returning the postreaction data that was created (the user and the reaction combo that was added)
            post.reactions.add(postreaction)

            serializer = PostReactionSerializer(
                postreaction, context={'request': request})

            return Response(serializer.data)

        except PostReactions.DoesNotExist as ex:
            # If we didn't find a reaction and user combination that already exists, then we need to create that from the reaction and user

            postreaction = PostReactions()
            postreaction.reaction = reaction
            postreaction.user = user

            # Try saving the postreaction record THEN we add this new postreaction to the post, returning the postreaction data that was created (the user and the reaction combo that was added)
            try:
                postreaction.save()
                post.reactions.add(postreaction)

                serializer = PostReactionSerializer(
                    postreaction, context={'request': request})

                return Response(serializer.data)

            except Exception as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
