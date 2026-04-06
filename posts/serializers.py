from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    author_avatar = serializers.ImageField(source="author.avatar", read_only=True)

    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    liked_by_user = serializers.SerializerMethodField()

    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "author_avatar",
            "content",
            "image",
            "likes_count",
            "liked_by_user",
            "comments_count",
            "created_at",
        ]

        read_only_fields = ["author"]

    def get_liked_by_user(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return obj.likes.filter(user=request.user).exists()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.name", read_only=True)
    avatar = serializers.ImageField(source="user.avatar", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "username", "avatar", "content", "created_at"]

        read_only_fields = ["user"]
