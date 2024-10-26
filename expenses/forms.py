from django import forms
from .models import Category, Expense

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'date', 'category']