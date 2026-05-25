from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    author_avatar = serializers.ImageField(source="author.avatar", read_only=True)

    image = serializers.ImageField(required=False, allow_null=True)

    image_url = serializers.SerializerMethodField()

    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    liked_by_user = serializers.SerializerMethodField()

    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    is_following_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "author_avatar",
            "is_following_author",
            "content",
            "image",
            "image_url",
            "likes_count",
            "liked_by_user",
            "comments_count",
            "created_at",
        ]

        read_only_fields = ["author"]

    def get_image_url(self, obj):
        request = self.context.get("request")

        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)

    def get_liked_by_user(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return obj.likes.filter(user=request.user).exists()

    def validate_image(self, value):
        if not value:
            return value

        if not value.content_type.startswith("image/"):
            raise serializers.ValidationError(
                "Apenas arquivos de imagem são permitidos."
            )

        valid_extensions = ["jpg", "jpeg", "png", "gif", "webp"]
        ext = value.name.split(".")[-1].lower()

        if value.size > 15 * 1024 * 1024:
            raise serializers.ValidationError("Imagem muito grande (Max 5MB)")

        return value

    def get_is_following_author(self, obj):

        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        if obj.author == request.user:
            return False

        return obj.author.followers.filter(followers=request.user).exists()


class CommentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username", read_only=True)

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "user", "username", "avatar", "content", "created_at"]

        read_only_fields = ["user", "username", "avatar"]

    def create(self, validated_data):
        # Captura username e avatar do usuário autenticado
        validated_data["username"] = self.context["request"].user.username
        if self.context["request"].user.avatar:
            validated_data["avatar"] = self.context["request"].user.avatar
        return super().create(validated_data)

    def get_avatar(self, obj):
        request = self.context.get("request")

        if obj.user.avatar and request:
            return request.build_absolute_uri(obj.user.avatar.url)

        return None
