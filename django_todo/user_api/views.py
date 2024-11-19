from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import PasswordSerializer, UserSerializer


# Viewset Classes
# ===============
class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["POST"], permission_classes=[])
    def register(self, request):
        # Validate request data
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            pswd_serializer = PasswordSerializer(data=request.data)

            if pswd_serializer.is_valid():
                # Create user
                User.objects.create_user(
                    username=serializer.validated_data["username"],
                    password=pswd_serializer.validated_data["password"],
                    email=serializer.validated_data["email"]
                )
                return Response(status=status.HTTP_201_CREATED)

            else:
                return Response(
                    pswd_serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["PUT"])
    def change_password(self, request):
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
