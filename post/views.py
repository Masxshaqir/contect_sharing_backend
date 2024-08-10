from .models import Post
from .serializer import UpdatePostSerializer, addPostSerializer
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
                    "title", "category", "hashtag", "contect", "post_image", "post_time"
                )
            )
            for i in all_posts:
                i["post_image"] = (
                    request.scheme + "://" + request.get_host() + "/" + i["post_image"]
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
