from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from .forms import CategoryForm, ExpenseForm
from django.db.models import Sum
import datetime
from collections import defaultdict

def summary_dashboard(request):
    # Get all expenses for the current user
    expenses = Expense.objects.filter(user=request.user)

    # Calculate total expenses
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Group expenses by category
    category_summaries = expenses.values('category__name').annotate(total=Sum('amount'))

    # Calculate monthly expenses for the current year
    current_year = datetime.datetime.now().year
    monthly_expenses = defaultdict(float)

    for expense in expenses.filter(date__year=current_year):
        month = expense.date.strftime('%B')  # Get month name (e.g., 'January')
        monthly_expenses[month] += float(expense.amount)  # Convert to float to avoid type issues

    context = {
        'total_expenses': float(total_expenses),  # Convert total to float for consistency
        'category_summaries': category_summaries,
        'monthly_expenses': dict(monthly_expenses),  # Convert to dict for easy template use
        'current_year': current_year,
    }
    return render(request, 'dashboard.html', context)

# List categories
@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'category/category_list.html', {'categories': categories})

@login_required
def category_detail(request, slug):
    # Retrieve the category for the logged-in user
    category = get_object_or_404(Category, slug=slug, user=request.user)
    return render(request, 'category/category_detail.html', {'category': category})

# Add new category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/add_category.html', {'form': form})

# Edit category
@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/edit_category.html', {'form': form})

# Delete category
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/delete_category.html', {'category': category})

# expense list
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)  # Only show logged-in user's expenses
    return render(request, 'expense/expense_list.html', {'expenses': expenses})

# Add Expense
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Link expense to logged-in user
            expense.save()
            return redirect('expense_list')  # Update this with your actual list view name
    else:
        form = ExpenseForm()
    return render(request, 'expense/add_expense.html', {'form': form})

# edit expense
@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)  # Only allow user's own expense
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense/edit_expense.html', {'form': form})

# delete expense
@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expense/delete_expense.html', {'expense': expense})