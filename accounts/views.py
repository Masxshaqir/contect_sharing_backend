from post.models import Post, Comment, Vote
from rest_framework import status
from accounts.serializer import *
from django.http import JsonResponse
from contect_sharing import settings
from django.db import transaction
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib import auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


def get_posts_per_user(request, user):
    posts = list(
        Post.objects.filter(user=user.id).values(
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
    )
    for i in posts:
        i["post_image"] = (
            (request.scheme + "://" + request.get_host() + "/" + i["post_image"])
            if i["post_image"]
            else ""
        )
    return posts

def get_posts(request):
    posts = list(
        Post.objects.all().values(
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
    )
    for i in posts:
        i["post_image"] = (
            (request.scheme + "://" + request.get_host() + "/" + i["post_image"])
            if i["post_image"]
            else ""
        )
    return posts


def get_comments_per_post(post):
    comments=list(
        Comment.objects.filter(post=post).values(
            "id",
            "comment",
            "comment_time",
            "user__email",
            "user__first_name",
            "user__last_name",
        )
    )
    return comments

def get_votes_per_post(post):
    all_votes=list(
                Vote.objects.filter(post=post).values(
                    'id',
                    "vote",
                    "vote_time",
                    "vote_update_time",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                )
            )
    vote_counts =  Vote.objects.filter(post=post).count()
    return all_votes ,vote_counts

@api_view(["POST"])
def register(request):
    try:
        with transaction.atomic():
            account_serializer = UserSerializer(data=request.data)

            if account_serializer.is_valid():
                user = account_serializer.save()
                user = {
                    "id": user.id,
                    "last_login": user.last_login,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "date_joined": user.date_joined,
                    "email": user.email,
                }

                return JsonResponse({"result": user}, safe=False, status=200)
            else:
                return JsonResponse(
                    account_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["POST"])
def signin(request):
    try:
        with transaction.atomic():
            logi_serializer = AuthTokenSerializer(data=request.data)

            if logi_serializer.is_valid():
                email = logi_serializer.validated_data["email"]
                password = logi_serializer.validated_data["password"]
                user = auth.authenticate(email=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)
                    user_data = {
                        "last_login": user.last_login,
                        "date_joined": user.date_joined,
                        "email": user.email,
                        "token": token.key,
                    }
                    return JsonResponse({"result": user_data}, safe=False, status=200)
                else:
                    return JsonResponse(
                        {"result": "User is not Authenticated"}, safe=False, status=400
                    )
            else:
                return JsonResponse(
                    logi_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:

        with transaction.atomic():
            user = User.objects.filter(id=request.user.id)
            if user:
                token = Token.objects.filter(user=request.user.id).first()
                auth.logout(request)
                if token:
                    token.delete()
            return JsonResponse({"result": "logged out"}, safe=False, status=200)
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    try:
        user = User.objects.get(email=request.data["email"])
        posts = get_posts_per_user(request,user)
    
        for i in posts:
            i["comments"]= get_comments_per_post(i['id'])
            i["all_votes"] , i["vote_counts"] = get_votes_per_post(i['id'])

        user_data = {
            "last_login": user.last_login,
            "date_joined": user.date_joined,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "posts": posts,
        }
        return JsonResponse({"result": user_data}, safe=False, status=200)

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        with transaction.atomic():
            user_obj = User.objects.get(id=request.user.id)
            update_AccountSerializer = updateAccountSerializer(
                user_obj, data=request.data, partial=True
            )
            if update_AccountSerializer.is_valid():
                update_AccountSerializer.save()

                return JsonResponse(
                    {"result": "Updated Succefully"}, safe=False, status=200
                )
            else:
                return JsonResponse(
                    update_AccountSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    try:
        all_users = list(
            User.objects.exclude(id=request.user.id)
            .exclude(is_superuser=True)
            .exclude(
                id__in=Friend.objects.filter(follower=request.user.id).values(
                    "followed"
                )
            )
            .values("first_name", "last_name", "email")
        )
        return JsonResponse({"result": all_users}, safe=False, status=200)

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_following_users(request):
    try:
        following_users = list(
            User.objects.filter(
                id__in=Friend.objects.filter(follower=request.user).values("followed")
            ).values("first_name", "last_name", "email")
        )

        return JsonResponse({"result": following_users}, safe=False, status=200)

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_friend(request):
    try:
        with transaction.atomic():
            request.data["follower"] = request.user.id
            request.data["followed"] = User.objects.filter(
                email=request.data["followed_email"]
            ).values("id")[0]["id"]
            add_Friend = addFriendSerializer(data=request.data)

            if add_Friend.is_valid():
                add_Friend.save()
                return JsonResponse({"result": "followed"}, safe=False, status=200)
            else:
                return JsonResponse(
                    add_Friend.errors, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_friend(request):
    try:
        with transaction.atomic():
            request.data["follower"] = request.user.id
            request.data["followed"] = User.objects.filter(
                email=request.data["followed_email"]
            ).values("id")[0]["id"]

            Friend.objects.get(
                follower=request.data["follower"], followed=request.data["followed"]
            ).delete()

            return JsonResponse({"result": "followed"}, safe=False, status=200)

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)
