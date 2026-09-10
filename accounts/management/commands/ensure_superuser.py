from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    help = (
        "Cria um superusuario a partir das variaveis de ambiente "
        "DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL e DJANGO_SUPERUSER_PASSWORD, "
        "sem fazer nada se as variaveis nao estiverem definidas ou o usuario ja existir."
    )

    def handle(self, *args, **options):
        import os

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME/PASSWORD nao definidos, pulando.")
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Usuario '{username}' ja existe, pulando.")
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' criado."))
        except IntegrityError:
            self.stdout.write(f"Usuario '{username}' ja existe (corrida com outro processo), pulando.")
