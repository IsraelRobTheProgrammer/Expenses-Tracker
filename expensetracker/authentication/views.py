from collections.abc import Callable, Iterable, Mapping
from typing import Any
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

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send(fail_silently=False)


# Create your views here.


class User_Validation_View(View):
    def post(self, request):
        data = json.loads(request.body)
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
                EmailThread(email).start()
                messages.success(
                    request, "Please check your email to activate your account"
                )
                return render(request, "auth/register.html")


reg_view = Register_View.as_view()


class Activation_View(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect("login" + "?message=" + "user already activated")

            if user.is_active:
                return redirect("login")

            user.is_active = True
            user.save()

            messages.success(request, "Account Activated Successfully, Please Login!")
            return redirect("login")
        except Exception as e:
            print("error", e)
            messages.info(request, "Something Went Wrong")
        return redirect("login")


activation_view = Activation_View.as_view()


class LoginView(View):
    def get(self, request):
        print(request.body, "request")
        return render(request, "auth/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
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


class RequestResetPswdView(View):
    def get(self, request):
        return render(request, "auth/forgot_password.html")

    def post(self, request):
        email = request.POST["email"]
        context = {"email": email, "emailValue": email}
        print(validate_email(email), "email val")
        if not validate_email(email):
            messages.error(request, "Invalid Email")
            return render(request, "auth/forgot_password.html", context)

        # path_to_view
        # - get current domain
        # - join the current relative url to verification view
        #  - encode the uid
        #  - token
        # current_site =  get_current_site(request)
        # email_body = {
        #     "user":user,
        #     "domain":current_site.domain,
        #     "uid":urlsafe_base64_encode(force_bytes(user.pk)),
        #     "token": token_generator.make_token(user)

        # }
        # user = request.objects.filter(email=email)
        # print(user,"first user")
        user_query = User.objects.filter(email=email)
        if user_query.exists():
            user = user_query[0]
            try:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse(
                    "reset",
                    kwargs={
                        "uidb64": uidb64,
                        "token": PasswordResetTokenGenerator().make_token(user),
                    },
                )

                reset_url = "http://" + domain + link
                email_body = (
                    "Hi "
                    + user.username
                    + " Please use this link to reset your account password\n"
                    + reset_url
                )
                email = EmailMessage(
                    "Password Reset",  # email_subject
                    email_body,
                    "noreply@gmail.com",
                    [user.email],
                )
                EmailThread(email).start()
                messages.success(request, "Reset Email Sent")
            except Exception as e:
                messages.error(request, "Something Went Wrong, Please Try Again")
                print(e)
                return render(request, "auth/forgot_password.html", context)

        else:
            messages.error(request, "Email does not exist")
            return render(request, "auth/forgot_password.html")

        return render(request, "auth/forgot_password.html")


request_reset = RequestResetPswdView.as_view()


class ResetPswdView(View):
    def get(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            # print(PasswordResetTokenGenerator().check_token(user, token), "PSWD")

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, "Reset link has expired, please request a new one"
                )
                return render(request, "auth/forgot_password.html")
        except Exception as e:
            messages.info(request, "Reset link is invalid, please request a new one")
            print("Error:", e)
            return render(request, "auth/forgot_password.html")

        return render(request, "auth/reset_password.html", context)

    def post(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}

        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "auth/reset_password.html", context)

        if len(password) < 6:
            messages.error(request, "Passwords too short")
            return render(request, "auth/reset_password.html", context)

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            user.set_password(password)
            user.save()

            messages.success(request, "Password reset successfull, Please Login")
            return redirect("login")
        except Exception as e:
            messages.info(request, "Something went wrong, Try Again")
            print(e)
            return render(request, "auth/reset_password.html", context)


reset_password = ResetPswdView.as_view()
