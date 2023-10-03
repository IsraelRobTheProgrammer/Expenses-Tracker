from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
import json


# Create your views here.


class User_Validation_View(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse(
                {"user_err": "username should only have alphanumeric characters"},
                status=400,
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"user_err": "username already in use"},
                status=409,
            )

        return JsonResponse({"username_valid": True})


user_val_view = User_Validation_View.as_view()


class Register_View(View):
    def get(self, request):
        return render(request, "auth/register.html")


reg_view = Register_View.as_view()
