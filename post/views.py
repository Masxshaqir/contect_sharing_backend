from .models import Post, Comment
from .serializer import UpdatePostSerializer, addCommentSerializer, addPostSerializer
from rest_framework import status
from accounts.serializer import *
from django.http import JsonResponse
from contect_sharing import settings
from django.db import transaction
from rest_framework.authtoken.models import Token

from django.contrib import auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def get_all_posts(request):
    try:
        with transaction.atomic():

            all_posts = list(
                Post.objects.all().values(
                    "id","title", "category", "hashtag", "contect", "post_image", "post_time"
                )
            )
            for i in all_posts:
                i["post_image"] = (
                    request.scheme + "://" + request.get_host() + "/" + i["post_image"]
                )
                i["comments"] = list(
                Comment.objects.filter(post=i["id"]).values('id',"comment", "comment_time", "user__email","user__first_name","user__last_name")
                )
                
            return JsonResponse({"result": all_posts}, safe=False, status=200)
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_post(request):
    try:
        with transaction.atomic():
            request.data["user"] = request.user.id
            new_postSerializer = addPostSerializer(data=request.data)
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


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_post(request):
    try:
        with transaction.atomic():
            post_obj = Post.objects.get(id=request.data["id"])
            Update_PostSerializer = UpdatePostSerializer(
                post_obj, data=request.data, partial=True
            )
            if Update_PostSerializer.is_valid():
                Update_PostSerializer.save()

                return JsonResponse(
                    {"result": "Updated Succefully"}, safe=False, status=200
                )
            else:
                return JsonResponse(
                    Update_PostSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


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


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_comment(request):
    try:
        with transaction.atomic():
            if Comment.objects.get(post=request.data["post"]):

                comment_obj = Comment.objects.get(id=request.data["id"])
                if not comment_obj:
                    return JsonResponse(
                        {"result": "you can't edit this comment"},
                        safe=False,
                        status=400,
                    )
                Update_CommentSerializer = UpdatePostSerializer(
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
                    {"result": "you can't edit this comment"}, safe=False, status=400
                )

    except Exception as error:
        return JsonResponse({"result": str(error)}, safe=False, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request):
    try:
        with transaction.atomic():
            if Comment.objects.get(post=request.data["post"]):

                comment_obj = Comment.objects.get(id=request.data["id"],user=request.user.id)
                if not comment_obj:
                    return JsonResponse(
                        {"result": "you can't delete this comment"},
                        safe=False,
                        status=400,
                    )
                Comment.objects.get(id=request.data["id"],post=request.data["post"],user=request.user.id).delete()
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



