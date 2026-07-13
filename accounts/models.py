from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/Avatar_default.png", null=True, blank=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Follow(models.Model):

    followers = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="following"
    )

    following = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="followers"
    )

    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("followers", "following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"
