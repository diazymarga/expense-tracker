from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm

def expense_list(request):
    # Fetch all expenses initially
    expenses = Expense.objects.all()

    # Get filter parameters
    filter_by = request.GET.get('filter_by', '')
    filter_value = request.GET.get('filter_value', '')

    # Apply filters based on selection
    if filter_by == 'category' and filter_value:
        expenses = expenses.filter(category__icontains=filter_value)
    elif filter_by == 'date' and filter_value:
        expenses = expenses.filter(date=filter_value)
    elif filter_by == 'amount' and filter_value:
        try:
            amount = float(filter_value)
            expenses = expenses.filter(amount=amount)
        except ValueError:
            # Ignore invalid amounts
            pass

    # Render the filtered data
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

from django.shortcuts import get_object_or_404

def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})
