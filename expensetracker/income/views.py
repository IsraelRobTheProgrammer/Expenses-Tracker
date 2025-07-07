from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userpreferences.models import UserPreference

# Create your views here.


@csrf_exempt
def search_income(request):
    if request.method == "POST":
        print("in post method")
        search_str = json.loads(request.body).get("searchText")

        income = (
            Income.objects.filter(amount__startswith=search_str, owner=request.user)
            | Income.objects.filter(date__startswith=search_str, owner=request.user)
            | Income.objects.filter(desc__icontains=search_str, owner=request.user)
            | Income.objects.filter(
                source__icontains=search_str, owner=request.user
            )
        )

        data = income.values()

        return JsonResponse(list(data), safe=False)
    return redirect("income_homepage")


@login_required(login_url="/auth/login")
def index(request):
    income = Income.objects.filter(owner=request.user)

    paginator = Paginator(income, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    currency = UserPreference.objects.get(user=request.user).currency 
    context = {
        "income": income,
        "page_obj": page_obj,
        "currency": currency,
    }
    return render(request, "income/index.html", context)


def add_income(request):
    sources = Source.objects.all()
    user_income = Income.objects.filter(owner=request.user)
    context = {"sources": sources, "fieldValues": request.POST}

    if request.method == "POST":
        amount = request.POST["amount"]
        desc = request.POST["desc"]
        date = request.POST["income_date"]
        source = request.POST["source"]
        if not amount:
            messages.error(request, "Amount Is Required")
            return render(request, "income/add_income.html", context)
        if not desc:
            messages.error(request, "Description Is Required")
            return render(request, "income/add_income.html", context)
        Income.objects.create(
            amount=amount,
            date=date,
            source=source,
            desc=desc,
            owner=request.user,
        )
        messages.success(request, "income saved successfully")
        return redirect("income_homepage")

    return render(request, "income/add_income.html", context)


def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()

    context = {
        "fieldValues": income,
        "sources": sources,
        "income": income,
    }

    if request.method == "POST":
        amount = request.POST["amount"]
        desc = request.POST["desc"]
        date = request.POST["income_date"]
        source = request.POST["source"]
        if not amount:
            messages.error(request, "Amount Is Required")
            return render(request, "income/edit_income.html", context)
        if not desc:
            messages.error(request, "Description Is Required")
            return render(request, "income/edit_income.html", context)

        income.amount = amount
        income.source = source
        income.desc = desc
        income.date = date

        income.save()

        messages.success(request, "Record edited successfully")
        return redirect("income_homepage")

    return render(request, "income/edit_income.html", context)


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Record deleted succesfully")
    return redirect("income_homepage")
