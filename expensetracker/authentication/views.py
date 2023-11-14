from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from validate_email import validate_email

from django.contrib import messages

from django.core.mail import EmailMessage
from django.contrib import auth

from django.urls import reverse

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator

# Create your views here.


class User_Validation_View(View):
    def post(self, request):
        data = json.loads(request.body)
        # print(data)
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


class Email_Validation_View(View):
    def post(self, request):
        data = json.loads(request.body)
        # print(data)
        email = data["email"]

        if not validate_email(email):
            return JsonResponse(
                {"email_err": "Invalid Email"},
                status=400,
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_err": "email already in use"},
                status=409,
            )

        return JsonResponse({"email_valid": True})


email_val_view = Email_Validation_View.as_view()


class Register_View(View):
    def get(self, request):
        return render(request, "auth/register.html")

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {"fieldValues": request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    print("too short")
                    messages.error(request, "Password too short")
                    return render(request, "auth/register.html", context)
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.is_active = False

                user.save()

                # path_to_view
                # - get current domain
                # - join the current relative url to verification view
                #  - encode the uid
                #  - token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse(
                    "activate",
                    kwargs={
                        "uidb64": uidb64,
                        "token": token_generator.make_token(user),
                    },
                )
                print(domain, "domain")
                print(link, "link")
                activate_url = "http://" + domain + link

                email_body = (
                    "Hi "
                    + user.username
                    + " Please use this link to verify your account\n"
                    + activate_url
                )
                email = EmailMessage(
                    "Activate Your Account",  # email_subject
                    email_body,
                    "noreply@gmail.com",
                    [user.email],
                )
                email.send(fail_silently=False)
                messages.success(request, "Account Created Successfully")
                return render(request, "auth/register.html")


reg_view = Register_View.as_view()


class Verification_View(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            print(id, "id")
            print(user, "user")

            if not token_generator.check_token(user, token):
                print("checking token")
                return redirect("login" + "?message=" + "user already activated")

            if user.is_active:
                print("checking active user")
                return redirect("login")

            print("b4 active")
            user.is_active = True
            user.save()

            messages.success(request, "Account Activated Successfully!")
            return redirect("login")
        except Exception as e:
            print(e)
            print("An Error Occured")
        return redirect("login")


verification_view = Verification_View.as_view()


class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                print(user.get_username(), "username")
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request,
                        "Welcome, " + user.get_username() + " you are now logged in",
                    )
                    return redirect("expenses_homepage")
                messages.error(
                    request,
                    "Account not active please check your email for a verification link",
                )
                return render(request, "auth/login.html")

            messages.error(
                request,
                "Invalid Credentials, try again",
            )
            return render(request, "auth/login.html")

        messages.error(
            request,
            "Please Enter All Fields",
        )
        return render(request, "auth/login.html")


login_view = LoginView.as_view()


class LogOutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "LogOut Successfully")
        return redirect("login")


log_out_view = LogOutView.as_view()
