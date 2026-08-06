from django import forms

from .models import Transaction

INPUT_CLASSES = "form-control"


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["category", "description", "amount", "date", "notes"]
        widgets = {
            "category": forms.Select(attrs={"class": INPUT_CLASSES}),
            "description": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "amount": forms.NumberInput(attrs={"class": INPUT_CLASSES, "step": "0.01", "min": "0"}),
            "date": forms.DateInput(attrs={"class": INPUT_CLASSES, "type": "date"}),
            "notes": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["category"].queryset = user.categories.all()
