from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Q


from .models import Post, Like
from accounts.models import Follow
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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

        serializer = CommentSerializer(data=request.data, context={"request": request})

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, post=post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):

        post = self.get_object()

        comments = post.comments.all().order_by("-created_at")

        serializer = CommentSerializer(
            comments, many=True, context={"request": request}
        )

        return Response(serializer.data)

    def get_serializer_context(self):

        context = super().get_serializer_context()

        context["request"] = self.request
        return context

    def get_queryset(self):

        queryset = Post.objects.select_related("author").prefetch_related(
            "likes", "comments"
        )

        # Apenas para o feed
        if self.action == "list":

            following_ids = Follow.objects.filter(
                followers=self.request.user
            ).values_list("following_id", flat=True)

            queryset = queryset.filter(
                Q(author=self.request.user) | Q(author__id__in=following_ids)
            )

        return queryset.order_by("-created_at")

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):

        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(post=post, user=request.user).first()

        if like:
            like.delete()
            liked = False
        else:
            Like.objects.create(post=post, user=request.user)
            liked = True

        return Response({"liked": liked, "likes_count": post.likes.count()})

    @action(detail=False, methods=["get"])
    def explore(self, request):

        posts = (
            Post.objects.select_related("author")
            .prefetch_related("likes", "comments")
            .exclude(author=request.user)
            .order_by("-created_at")
        )

        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my_posts(self, request):

        posts = (
            Post.objects.filter(author=request.user)
            .select_related("author")
            .prefetch_related("likes", "comments")
            .order_by("-created_at")
        )

        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data)
