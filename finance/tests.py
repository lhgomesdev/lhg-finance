from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import TransactionForm
from .models import Category, Transaction
from .signals import DEFAULT_CATEGORIES

User = get_user_model()


class DefaultCategoriesSignalTests(TestCase):
    def test_creates_default_categories_for_new_user(self):
        user = User.objects.create_user(username="alice", password="senha-forte-123")

        self.assertEqual(user.categories.count(), len(DEFAULT_CATEGORIES))

    def test_default_categories_have_expected_types(self):
        user = User.objects.create_user(username="alice", password="senha-forte-123")

        expected_types = {type_ for _, type_, _ in DEFAULT_CATEGORIES}
        actual_types = set(user.categories.values_list("type", flat=True))
        self.assertEqual(actual_types, expected_types)

    def test_does_not_recreate_categories_on_user_update(self):
        user = User.objects.create_user(username="alice", password="senha-forte-123")

        user.first_name = "Alice"
        user.save()

        self.assertEqual(user.categories.count(), len(DEFAULT_CATEGORIES))


class TransactionFormTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="senha-forte-123")
        self.other = User.objects.create_user(username="other", password="senha-forte-123")

    def test_category_queryset_limited_to_given_user(self):
        form = TransactionForm(user=self.owner)

        queryset_users = set(form.fields["category"].queryset.values_list("user", flat=True))
        self.assertEqual(queryset_users, {self.owner.pk})

    def test_cannot_submit_another_users_category(self):
        other_category = self.other.categories.first()
        form = TransactionForm(
            user=self.owner,
            data={
                "category": other_category.pk,
                "description": "Compra",
                "amount": "10.00",
                "date": "2026-01-01",
                "notes": "",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)


class TransactionPermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="senha-forte-123")
        self.other = User.objects.create_user(username="other", password="senha-forte-123")
        self.category = self.owner.categories.filter(type=Category.Type.EXPENSE).first()
        self.transaction = Transaction.objects.create(
            user=self.owner,
            category=self.category,
            description="Mercado",
            amount=Decimal("50.00"),
            date="2026-01-05",
        )

    def test_owner_can_access_update_view(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("transaction-update", args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_access_update_view(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("transaction-update", args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 404)

    def test_other_user_cannot_delete_transaction(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse("transaction-delete", args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Transaction.objects.filter(pk=self.transaction.pk).exists())

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse("transaction-update", args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


class DashboardBalanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="senha-forte-123")
        self.income_category = self.user.categories.filter(type=Category.Type.INCOME).first()
        self.expense_category = self.user.categories.filter(type=Category.Type.EXPENSE).first()
        self.client.force_login(self.user)

    def test_balance_is_income_minus_expense(self):
        today = timezone.localdate()
        Transaction.objects.create(
            user=self.user, category=self.income_category,
            description="Salário", amount=Decimal("3000.00"), date=today,
        )
        Transaction.objects.create(
            user=self.user, category=self.expense_category,
            description="Mercado", amount=Decimal("500.00"), date=today,
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["income"], Decimal("3000.00"))
        self.assertEqual(response.context["expense"], Decimal("500.00"))
        self.assertEqual(response.context["balance"], Decimal("2500.00"))

    def test_dashboard_ignores_other_users_transactions(self):
        other = User.objects.create_user(username="bob", password="senha-forte-123")
        Transaction.objects.create(
            user=other, category=other.categories.filter(type=Category.Type.INCOME).first(),
            description="Salário do Bob", amount=Decimal("9999.00"), date=timezone.localdate(),
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["income"], 0)
        self.assertEqual(response.context["balance"], 0)


class TransactionListMonthFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="senha-forte-123")
        self.category = self.user.categories.filter(type=Category.Type.EXPENSE).first()
        self.client.force_login(self.user)
        Transaction.objects.create(
            user=self.user, category=self.category,
            description="Janeiro", amount=Decimal("100.00"), date="2026-01-15",
        )
        Transaction.objects.create(
            user=self.user, category=self.category,
            description="Fevereiro", amount=Decimal("200.00"), date="2026-02-15",
        )

    def test_lists_only_transactions_from_selected_month(self):
        response = self.client.get(reverse("transaction-list"), {"year": 2026, "month": 1})

        descriptions = [t.description for t in response.context["transactions"]]
        self.assertEqual(descriptions, ["Janeiro"])

    def test_invalid_month_falls_back_to_today(self):
        response = self.client.get(reverse("transaction-list"), {"year": 2026, "month": 13})

        self.assertEqual(response.status_code, 200)


class HealthzTests(TestCase):
    def test_healthz_is_public_and_ok(self):
        response = self.client.get(reverse("healthz"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")
