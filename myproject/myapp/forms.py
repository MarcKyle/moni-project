from django import forms
from .models import Transaction
from django.core.exceptions import ValidationError

class SimpleTransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    is_added = forms.ChoiceField(choices=[(True, 'Deposit'), (False, 'Withdraw')])
    description = forms.CharField(max_length=255, required=False)

class TransactionModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'is_added', 'description']
        labels = {
            'is_added': 'Type (Deposit/Withdraw)'
        }
        widgets = {
            'is_added': forms.Select(choices=[(True, 'Deposit'), (False, 'Withdraw')])
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_added = cleaned_data.get('is_added')
        amount = cleaned_data.get('amount')
        if self.user and str(is_added) == 'False':  # Withdraw
            transactions = Transaction.objects.filter(user=self.user)
            balance = sum(t.amount if t.is_added else -t.amount for t in transactions)
            if amount and amount > balance:
                raise ValidationError("You cannot withdraw more than your current balance.")
        return cleaned_data
