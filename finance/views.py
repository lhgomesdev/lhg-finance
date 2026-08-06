import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TransactionForm
from .models import Category, Transaction


@login_required
def dashboard(request):
    today = timezone.localdate()
    transactions = (
        Transaction.objects.filter(user=request.user, date__year=today.year, date__month=today.month)
        .select_related("category")
    )

    income = transactions.filter(category__type=Category.Type.INCOME).aggregate(total=Sum("amount"))["total"] or 0
    expense = transactions.filter(category__type=Category.Type.EXPENSE).aggregate(total=Sum("amount"))["total"] or 0

    expense_by_category = (
        transactions.filter(category__type=Category.Type.EXPENSE)
        .values("category__name", "category__color")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    context = {
        "transactions": transactions[:10],
        "income": income,
        "expense": expense,
        "balance": income - expense,
        "chart_labels": json.dumps([row["category__name"] for row in expense_by_category]),
        "chart_colors": json.dumps([row["category__color"] for row in expense_by_category]),
        "chart_values": json.dumps([float(row["total"]) for row in expense_by_category]),
    }
    return render(request, "finance/dashboard.html", context)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "finance/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_selected_month(self):
        today = timezone.localdate()
        try:
            year = int(self.request.GET.get("year", today.year))
            month = int(self.request.GET.get("month", today.month))
            if not 1 <= month <= 12:
                raise ValueError
        except (TypeError, ValueError):
            year, month = today.year, today.month
        return year, month

    def get_queryset(self):
        year, month = self.get_selected_month()
        return (
            Transaction.objects.filter(user=self.request.user, date__year=year, date__month=month)
            .select_related("category")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year, month = self.get_selected_month()

        qs = self.get_queryset()
        income = qs.filter(category__type=Category.Type.INCOME).aggregate(total=Sum("amount"))["total"] or 0
        expense = qs.filter(category__type=Category.Type.EXPENSE).aggregate(total=Sum("amount"))["total"] or 0

        current = timezone.datetime(year, month, 1)
        prev_month = current - timezone.timedelta(days=1)
        next_month = current + timezone.timedelta(days=32)

        context.update({
            "year": year,
            "month": month,
            "income": income,
            "expense": expense,
            "balance": income - expense,
            "prev_year": prev_month.year,
            "prev_month": prev_month.month,
            "next_year": next_month.year,
            "next_month": next_month.month,
            "month_date": current.date(),
        })
        return context


class UserTransactionMixin(LoginRequiredMixin):
    model = Transaction
    success_url = reverse_lazy("transaction-list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class UserTransactionFormMixin(UserTransactionMixin):
    form_class = TransactionForm
    template_name = "finance/transaction_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TransactionCreateView(UserTransactionFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(UserTransactionFormMixin, UpdateView):
    pass


class TransactionDeleteView(UserTransactionMixin, DeleteView):
    template_name = "finance/transaction_confirm_delete.html"
