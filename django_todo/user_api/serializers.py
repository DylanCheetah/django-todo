from django.contrib.auth.models import User
from rest_framework import serializers


# Serializer Classes
# ==================
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "id", "username", "password", "email"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True}
        }


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, value):
        """
        Ensure that passwords are at least 8 characters long.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Passwords must be at least 8 characters long."
            )

        return value
