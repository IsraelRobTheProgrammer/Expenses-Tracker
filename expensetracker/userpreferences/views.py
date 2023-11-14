from django.shortcuts import render
import os
import json
from django.contrib import messages

from django.conf import settings
from .models import UserPreference

# Create your views here.


def index(request):
    exists = UserPreference.objects.filter(user=request.user).exists()

    user_preferences = UserPreference.objects.get(user=request.user) if exists else None
    print(user_preferences, "user")

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, "currencies.json")

    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({"name": k, "value": v})

    if request.method == "GET":
        return render(
            request,
            "preferences/index.html",
            {"currencies": currency_data, "user_preferences": user_preferences},
        )

    else:
        currency = request.POST["currency"]
        if exists:
            user_preferences.currency = currency  # type:ignore
            user_preferences.save()  # type:ignore
            messages.success(request, "Changes Saved")

        else:
            UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, "Changes Saved")

    return render(
        request,
        "preferences/index.html",
        {"currencies": currency_data, "user_preferences": user_preferences},
    )
