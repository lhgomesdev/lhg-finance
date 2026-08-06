from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("transacoes/", views.TransactionListView.as_view(), name="transaction-list"),
    path("transacoes/nova/", views.TransactionCreateView.as_view(), name="transaction-create"),
    path("transacoes/<int:pk>/editar/", views.TransactionUpdateView.as_view(), name="transaction-update"),
    path("transacoes/<int:pk>/excluir/", views.TransactionDeleteView.as_view(), name="transaction-delete"),
]
