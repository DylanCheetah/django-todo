from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from . import utils
from .serializers import (
    EmailSerializer,
    PasswordSerializer,
    PrivateUserSerializer,
    UserSerializer
)


# Viewset Classes
# ===============
class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("username")
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["POST"], permission_classes=[])
    def register(self, request):
        # Validate request data
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Create user
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                email=serializer.validated_data["email"],
                is_active=False
            )

            # Send verification email
            utils.send_verification_email(user)
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False,
            methods=["GET"],
            permission_classes=[],
            renderer_classes=[TemplateHTMLRenderer])
    def verify(self, request):
        # Validate params
        if "token" not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Verify user
        try:
            utils.verify_user(request.query_params["token"])
            return Response(
                {
                    "WEBSITE_NAME": settings.WEBSITE_NAME
                },
                template_name="user_api/verification_complete.html"
            )

        except Exception:
            return Response(
                {
                    "WEBSITE_NAME": settings.WEBSITE_NAME,
                    "WEBSITE_EMAIL": settings.WEBSITE_EMAIL
                },
                template_name="user_api/verification_failed.html"
            )

    @action(detail=False, methods=["PUT"], serializer_class=PasswordSerializer)
    def set_password(self, request):
        # Validate request data
        pswd_serializer = PasswordSerializer(data=request.data)

        if pswd_serializer.is_valid():
            # Update the user's password
            request.user.set_password(
                pswd_serializer.validated_data["password"]
            )
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                pswd_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["PUT"], serializer_class=EmailSerializer)
    def set_email(self, request):
        # Validate request data
        email_serializer = EmailSerializer(data=request.data)

        if email_serializer.is_valid():
            # Update the user's email address
            request.user.email = email_serializer.validated_data["email"]
            request.user.is_active = False
            request.user.save()

            # Send verification email
            utils.send_verification_email(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["DELETE"])
    def delete(self, request):
        # Delete the user
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"],
            serializer_class=PrivateUserSerializer)
    def me(self, request):
        # Serialize return user data
        user_serializer = PrivateUserSerializer(
            request.user,
            context={"request": request}
        )
        return Response(user_serializer.data)
