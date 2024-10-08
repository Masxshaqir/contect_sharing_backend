from accounts.views import get_comments_per_post, get_posts, get_votes_per_post
from .models import Post, Comment, Vote
from .serializer import (
    PostSerializer,
    UpdateCommentSerializer,
    UpdatePostSerializer,
    UpdateVoteSerializer,
    addCommentSerializer,
    addPostSerializer,
    addVoteSerializer,
)
from django.db.models import Avg
from rest_framework import status
from accounts.serializer import *
from django.http import JsonResponse
from contect_sharing import settings
from django.db import transaction
from rest_framework.authtoken.models import Token
from django.db.models import Count
from django.contrib import auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Post
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .filters import PostFilter


@swagger_auto_schema(
    method='GET',
    # manual_parameters=[auth_header],  # Add the Authorization header to Swagger
    # responses={200: 'Logged out', 400: 'Error occurred'}
)
@api_view(["GET"])
def get_all_posts(request):
    try:
        with transaction.atomic():

            all_posts = get_posts(request)
            for i in all_posts:
                
                i["comments"] = get_comments_per_post(i['id'])
                i["all_votes"] , i["vote_counts"] = get_votes_per_post(i['id'])
                
            return JsonResponse({"result": all_posts}, safe=False, status=200)
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)



auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)


@swagger_auto_schema(
    method='post',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=addPostSerializer,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_post(request):
    try:
        with transaction.atomic():
            data = request.data.copy()
            data["user"] = request.user.id
            new_postSerializer = addPostSerializer(data=data)
            if new_postSerializer.is_valid():
                new_postSerializer.save()

                return JsonResponse(
                    {"result": "Added Succefully"}, safe=False, status=200
                )
            else:
                return JsonResponse(
                    new_postSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)


@swagger_auto_schema(
    method='PUT',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=UpdatePostSerializer,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'},
    consumes=["multipart/form-data"]
)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_post(request):
    try:
        with transaction.atomic():
            post_obj = Post.objects.get(id=request.data["id"])
            if post_obj:

                if not (post_obj.user.id == request.user.id):
                    return JsonResponse(
                        {"result": "you can't edit this Post"},
                        safe=False,
                        status=400,
                    )

                Update_PostSerializer = UpdatePostSerializer(post_obj, data=request.data, partial=True)
                if Update_PostSerializer.is_valid():
                    Update_PostSerializer.save()

                    return JsonResponse(
                        {"result": "Updated Succefully"}, safe=False, status=200
                    )
                else:
                    return JsonResponse(
                        Update_PostSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return JsonResponse(
                    {"result": "Post not found"}, safe=False, status=400
                )

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)

post = openapi.Schema(
    type=openapi.TYPE_OBJECT,  # Define the body as an object
    properties={
        'post': openapi.Schema(type=openapi.TYPE_STRING, description='post id')  # Add the email field
    },
    required=['post'],  # Mark email as required
)

@swagger_auto_schema(
    method='DELETE',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=post,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'}
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post(request):
    try:
        with transaction.atomic():
            post_obj = Post.objects.get(id=request.data["post"])
            if post_obj:

                if not (post_obj.user.id == request.user.id):
                    return JsonResponse(
                        {"result": "you can't delete this Post"},
                        safe=False,
                        status=400,
                    )

                post_obj.delete()
                return JsonResponse(
                    {"result": "Deleted  Succefully"}, safe=False, status=200
                )
            else:
                return JsonResponse(
                    {"result": "Post not found"}, safe=False, status=400
                )

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)
    


auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)

comment_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Comment text'),
        'post': openapi.Schema(type=openapi.TYPE_STRING, description='Post ID'),
    },
    required=['comment', 'post'],  # Specify required fields
)

@swagger_auto_schema(
    method='POST',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=comment_body_schema,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'}
)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment(request):
    try:
        with transaction.atomic():
            request.data["user"] = request.user.id

            new_commentSerializer = addCommentSerializer(data=request.data)
            if new_commentSerializer.is_valid():
                new_commentSerializer.save()

                return JsonResponse(
                    {"result": "commented Succefully"}, safe=False, status=200
                )
            else:
                return JsonResponse(
                    new_commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)

auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)


@swagger_auto_schema(
    method='PUT',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=UpdateCommentSerializer,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'}
)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_comment(request):
    try:
        with transaction.atomic():
            comment_obj = Comment.objects.get(id=request.data["id"])
            if comment_obj:

                if not (comment_obj.user.id == request.user.id):
                    return JsonResponse(
                        {"result": "you can't edit this comment"},
                        safe=False,
                        status=400,
                    )

                Update_CommentSerializer = UpdateCommentSerializer(
                    comment_obj, data=request.data, partial=True
                )
                if Update_CommentSerializer.is_valid():
                    Update_CommentSerializer.save()

                    return JsonResponse(
                        {"result": "Updated Succefully"}, safe=False, status=200
                    )
                else:
                    return JsonResponse(
                        Update_CommentSerializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return JsonResponse(
                    {"result": "Comment not found"}, safe=False, status=400
                )

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)

id = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_STRING, description='Comment id'),
 
    },
    required=['id'],  # Specify required fields
)
@swagger_auto_schema(
    method='DELETE',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=id,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'}
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request):
    try:
        with transaction.atomic():
            comment_obj = Comment.objects.get(id=request.data["id"])
            if comment_obj:

                if not (comment_obj.user.id == request.user.id):
                    return JsonResponse(
                        {"result": "you can't delete this comment"},
                        safe=False,
                        status=400,
                    )
                comment_obj.delete()
                # Comment.objects.delete(id=request.data["id"])

                return JsonResponse(
                    {"result": "Deleted Succefully"}, safe=False, status=200
                )
            else:
                return JsonResponse(
                    {"result": "Comment not found"}, safe=False, status=400
                )

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)

data = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_STRING, description='Comment id'),
        'post' : openapi.Schema(type=openapi.TYPE_STRING, description='Post id'),
        'vote' : openapi.Schema(type=openapi.TYPE_INTEGER, description='Vote'),
    },
    required=['vote','post'],  # Specify required fields
)
@swagger_auto_schema(
    method='POST',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=data,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_update_vote(request):
    try:
        with transaction.atomic():

            if "id" in request.data:
                Vote_obj = Vote.objects.get(
                    post=request.data["post"],
                    user=request.user.id,
                    id=request.data["id"],
                )

                if Vote_obj:
                    if not (Vote_obj.user.id == request.user.id):
                        return JsonResponse(
                            {"result": "you can't edit this comment"},
                            safe=False,
                            status=400,
                        )
                    Update_VoteSerializer = UpdateVoteSerializer(
                        Vote_obj, data=request.data, partial=True
                    )
                    if Update_VoteSerializer.is_valid():
                        Update_VoteSerializer.save()

                        return JsonResponse(
                            {"result": "Updated Succefully"}, safe=False, status=200
                        )
                    else:
                        return JsonResponse(
                            Update_VoteSerializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return JsonResponse(
                        {"result": "vote not found"}, safe=False, status=400
                    )
            else:
                request.data["user"] = request.user.id

                new_voteSerializer = addVoteSerializer(data=request.data)
                if new_voteSerializer.is_valid():
                    new_voteSerializer.save()

                    return JsonResponse(
                        {"result": "voted Succefully"}, safe=False, status=200
                    )
                else:
                    return JsonResponse(
                        new_voteSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)

post = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
 
        'post' : openapi.Schema(type=openapi.TYPE_STRING, description='Post id'),
    
    },
    required=['post'],  # Specify required fields
)
@swagger_auto_schema(
    method='POST',
    manual_parameters=[auth_header],  # Include the Authorization header
    request_body=post,  # Define the request body inline
    responses={200: 'Success', 400: 'Error occurred'}
)
@api_view(["POST"])
def get_votes(request):
    try:
        with transaction.atomic():
            all_votes = list(
                Vote.objects.filter(post=request.data["post"]).values(
                    "vote",
                    "vote_time",
                    "vote_update_time",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                )
            )
            vote_counts = Vote.objects.filter(post=request.data["post"]).count()

            return JsonResponse(
                {"result": {"all_votes": all_votes, "vote_counts": vote_counts}},
                safe=False,
                status=200,
            )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)



@api_view(['GET'])
def get_all_hashtags(request):
    try:
        # Fetch all hashtags as a list of strings
        hashtags_list = Post.objects.values_list('hashtag', flat=True).distinct()
        
        # Use a set comprehension to extract and deduplicate hashtags
        all_hashtags = {tag for hashtags in hashtags_list for tag in hashtags.replace(' ', '').split('#') if tag}

        return JsonResponse({'all_hashtags': list(all_hashtags)}, safe=False, status=200)
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


auth_header = openapi.Parameter(
    'Authorization',  # Name of the header
    openapi.IN_HEADER,  # Location: header
    description="Token <user_token>",  # Description of the header
    type=openapi.TYPE_STRING,  # Data type
    required=True  # Required field
)

category_param = openapi.Parameter(
    'category',  # Name of the query parameter
    openapi.IN_QUERY,  # Location: query string
    description='Category of the post',  # Description of the query parameter
    type=openapi.TYPE_STRING,  # Data type
    required=False  # Optional field
)

title_param = openapi.Parameter(
    'title',  # Name of the query parameter
    openapi.IN_QUERY,  # Location: query string
    description='Title of the post',  # Description of the query parameter
    type=openapi.TYPE_STRING,  # Data type
    required=False  # Optional field
)

hashtag_param = openapi.Parameter(
    'hashtag',  # Name of the query parameter
    openapi.IN_QUERY,  # Location: query string
    description='Hashtag of the post',  # Description of the query parameter
    type=openapi.TYPE_STRING,  # Data type
    required=False  # Optional field
)

content_param = openapi.Parameter(
    'content',  # Name of the query parameter
    openapi.IN_QUERY,  # Location: query string
    description='Content of the post',  # Description of the query parameter
    type=openapi.TYPE_STRING,  # Data type
    required=False  # Optional field
)

post_time_param = openapi.Parameter(
    'post_time',  # Name of the query parameter
    openapi.IN_QUERY,  # Location: query string
    description='Post time',  # Description of the query parameter
    type=openapi.TYPE_STRING,  # Data type
    required=False  # Optional field
)

@swagger_auto_schema(
    method='GET',
    manual_parameters=[auth_header, category_param, title_param, hashtag_param, content_param, post_time_param],
    responses={200: 'Success', 400: 'Error occurred'}
)
@api_view(['GET'])
def post_filter_list(request):
    try:
        queryset = Post.objects.all()
        # Apply filtering
        filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
        filterset = PostFilter(request.GET, queryset=queryset)
        queryset = filterset.qs
        
        # Apply search and ordering
        search_fields = ['title', 'content', 'hashtag','category']
        ordering_fields = ['post_time', 'post_update_time', 'title', 'category']
        
        for backend in filter_backends:
            queryset = backend().filter_queryset(request, queryset, view=None)
        # Serialize the data
        serializer = PostSerializer(queryset, many=True)
        queryset = queryset.values(
            "id",
            "title",
            "category",
            "hashtag",
            "content",
            "post_image",
            "post_time",
            "user__first_name",
            "user__last_name",
            "user__email",
        )
        
        # Since you're using .values(), you don't need to serialize the data again
        all_posts = list(queryset)

        for i in all_posts:
            i["post_image"] = (
            (request.scheme + "://" + request.get_host() + "/" + i["post_image"])
            if i["post_image"]
            else ""
            )
            i["comments"] = get_comments_per_post(i['id'])
            i["all_votes"] , i["vote_counts"] = get_votes_per_post(i['id'])
            
        return JsonResponse({"result": all_posts}, safe=False, status=200)
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)