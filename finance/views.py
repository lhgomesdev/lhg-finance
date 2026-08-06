from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

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

    context = {
        "transactions": transactions[:10],
        "income": income,
        "expense": expense,
        "balance": income - expense,
    }
    return render(request, "finance/dashboard.html", context)
