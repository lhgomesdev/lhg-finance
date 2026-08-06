from django.conf import settings
from django.db import models


class Category(models.Model):
    class Type(models.TextChoices):
        INCOME = "IN", "Receita"
        EXPENSE = "EX", "Despesa"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=Type.choices)
    color = models.CharField(max_length=7, default="#6366f1")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name", "type")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    description = models.CharField(max_length=140)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.description} ({self.amount})"

    @property
    def type(self):
        return self.category.type
