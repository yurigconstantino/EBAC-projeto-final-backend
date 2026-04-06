from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):

        post = self.get_object()
        user = request.user

        like = Like.objects.filter(post=post, user=user).first()

        if like:
            like.delete()
            return Response({"liked": False, "likes_count": post.likes.count()})

        Like.objects.create(post=post, user=user)

        return Response({"liked": True, "likes_count": post.likes.count()})

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):

        post = self.get_object()

        serializer = CommentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, post=post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):

        post = self.get_object()

        comments = post.comments.all().order_by("created_at")

        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)
