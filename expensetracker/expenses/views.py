from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def search_expenses(request):
    if request.method == "POST":
        print("in post method")
        search_str = json.loads(request.body).get("searchText")

        expenses = (
            Expenses.objects.filter(amount__startswith=search_str, owner=request.user)
            | Expenses.objects.filter(date__startswith=search_str, owner=request.user)
            | Expenses.objects.filter(desc__icontains=search_str, owner=request.user)
            | Expenses.objects.filter(
                category__icontains=search_str, owner=request.user
            )
        )

        data = expenses.values()

        return JsonResponse(list(data), safe=False)
    return redirect("expenses_homepage")


@login_required(login_url="/auth/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)

    paginator = Paginator(expenses, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"expenses": expenses, "page_obj": page_obj}
    return render(request, "expenses/index.html", context)


def add_expenses(request):
    categories = Category.objects.all()
    user_expenses = Expenses.objects.filter(owner=request.user)
    context = {"categories": categories, "fieldValues": request.POST}

    if request.method == "POST":
        amount = request.POST["amount"]
        desc = request.POST["desc"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not amount:
            messages.error(request, "Amount Is Required")
            return render(request, "expenses/add_expenses.html", context)
        if not desc:
            messages.error(request, "Description Is Required")
            return render(request, "expenses/add_expenses.html", context)
        Expenses.objects.create(
            amount=amount,
            date=date,
            category=category,
            desc=desc,
            owner=request.user,
        )
        messages.success(request, "Expense saved successfully")
        return redirect("expenses_homepage")

    return render(request, "expenses/add_expenses.html", context)


def edit_expenses(request, id):
    expense = Expenses.objects.get(pk=id)
    categories = Category.objects.all()

    context = {
        "fieldValues": expense,
        "categories": categories,
        "expense": expense,
    }

    if request.method == "POST":
        amount = request.POST["amount"]
        desc = request.POST["desc"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not amount:
            messages.error(request, "Amount Is Required")
            return render(request, "expenses/edit_expenses.html", context)
        if not desc:
            messages.error(request, "Description Is Required")
            return render(request, "expenses/edit_expenses.html", context)

        expense.amount = amount
        expense.category = category
        expense.desc = desc
        expense.date = date
        expense.owner = request.user

        expense.save()

        messages.success(request, "Expense edited successfully")
        return redirect("expenses_homepage")

        # messages.info(request, "HANDLING POST FORM")
        # return render(request, "expenses/edit_expenses.html", context)

    return render(request, "expenses/edit_expenses.html", context)


def delete_expenses(request, id):
    expense = Expenses.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted succesfully")
    return redirect("expenses_homepage")
