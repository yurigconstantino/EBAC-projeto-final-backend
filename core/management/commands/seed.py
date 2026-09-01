import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

from posts.models import Post, Like, Comment

User = get_user_model()


class Command(BaseCommand):
    help = "Popula o banco com dados fake"

    def handle(self, *args, **kwargs):

        fake = Faker()

        self.stdout.write("Limpando banco")

        Comment.objects.all().delete()
        Like.objects.all().delete()
        Post.objects.all().delete()
        User.objects.all().delete()

        #Criar usuários
        self.stdout.write("Criando usuários")

        users = []

        for _ in range(20):
            user = User.objects.create_user(
                username=fake.user_name(), email=fake.email(), password="123456"
            )
            users.append(user)

        #Criar posts
        self.stdout.write("Criando posts")

        posts = []

        for user in users:

            for _ in range(random.randint(1, 5)):

                post = Post.objects.create(
                    author=user, content=fake.text(max_nb_chars=200)
                )

                posts.append(post)


        #Criar likes
        self.stdout.write("Criando likes")

        for post in posts:

            liked_users = random.sample(users, random.randint(0, len(users)))

            for user in liked_users:
                Like.objects.get_or_create(user=user, post=post)

        #Criar comentários
        self.stdout.write("Criando comentários")

        for post in posts:

            for _ in range(random.randint(0, 5)):

                Comment.objects.create(
                    user=random.choice(users), post=post, content=fake.sentence()
                )

        self.stdout.write(self.style.SUCCESS("Seed finalizado!"))
