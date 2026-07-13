from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    FollowingUserSerializer,
    UpdateProfileSerializer,
)
from django.contrib.auth import get_user_model
from .models import Follow

# Create your views here.
User = get_user_model()


class RegisterViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Usuario criado", "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(APIView):

    def post(self, request):
        selializer = LoginSerializer(data=request.data)

        selializer.is_valid(raise_exception=True)

        return Response(selializer.validated_data, status=status.HTTP_200_OK)


class MeViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serialiszer = UserSerializer(request.user)

        return Response(serialiszer.data)


class FollowToggleView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"erro": "Usuario não encontrado"}, status=404)

        if target_user == request.user:
            return Response(
                {
                    "erro": "Ta de sacanagem que voce quer seguri voce mesmo? Ta carente?"
                },
                status=400,
            )

        follow = Follow.objects.filter(
            followers=request.user, following=target_user
        ).first()

        if follow:
            follow.delete()

            return Response(
                {"following": False, "followers_count": target_user.followers.count()}
            )

        Follow.objects.create(followers=request.user, following=target_user)

        return Response(
            {"following": True, "followers_count": target_user.followers.count()}
        )


class FollowStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"erro": "Usuario não encontrado"}, status=404)

        is_following = Follow.objects.filter(
            follower=request.user, following=target_user
        ).exists()

        return Response(
            {
                "following": is_following,
                "followers_count": target_user.followers.count(),
            }
        )


class FollowingListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        follows = Follow.objects.filter(followers=request.user).select_related(
            "following"
        )

        users = [follow.following for follow in follows]

        serializer = FollowingUserSerializer(users, many=True, context={"request": request})

        return Response(serializer.data)


class UpdateProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        serializer = UpdateProfileSerializer(
            request.user, data=request.data, partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)
