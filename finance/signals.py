from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category

DEFAULT_CATEGORIES = [
    ("Salário", Category.Type.INCOME, "#22c55e"),
    ("Freelance", Category.Type.INCOME, "#10b981"),
    ("Outras Receitas", Category.Type.INCOME, "#84cc16"),
    ("Mercado", Category.Type.EXPENSE, "#ef4444"),
    ("Moradia", Category.Type.EXPENSE, "#f97316"),
    ("Transporte", Category.Type.EXPENSE, "#eab308"),
    ("Saúde", Category.Type.EXPENSE, "#ec4899"),
    ("Lazer", Category.Type.EXPENSE, "#8b5cf6"),
    ("Assinaturas", Category.Type.EXPENSE, "#6366f1"),
    ("Outras Despesas", Category.Type.EXPENSE, "#64748b"),
]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        Category.objects.bulk_create([
            Category(user=instance, name=name, type=type_, color=color)
            for name, type_, color in DEFAULT_CATEGORIES
        ])
