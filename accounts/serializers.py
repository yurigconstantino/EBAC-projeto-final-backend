from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "avatar", "bio"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email ou senha invalidos")

        if not user:
            raise serializers.ValidationError("Email ou senha invalidos")

        refresh = RefreshToken.for_user(user)

        return {
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar", "bio"]


class PublicUserSerializer(serializers.ModelSerializer):

    followers_count = serializers.IntegerField(source="followers.count", read_only=True)

    following_count = serializers.IntegerField(source="following.count", read_only=True)

    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "avatar",
            "followers_count",
            "following_count",
            "is_following",
        ]

    def get_is_following(self, obj):

        request = self.context.get("request")

        if not request or request.user.is_anonymos:
            return False

        return obj.followers.filter(follower=request.user).exists()


class FollowingUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "avatar"]

    def get_avatar(self, obj):

        request = self.context.get("request")

        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class UpdateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User

        fields = ["username", "email", "password", "avatar"]

    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)

        avatar = validated_data.get("avatar")

        if avatar:
            instance.avatar = avatar

        if password:
            instance.set_password(password)

        instance.save()

        return instance
