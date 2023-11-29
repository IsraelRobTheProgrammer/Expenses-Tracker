from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("register", views.reg_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.log_out_view, name="logout"),
    path("request_reset_password", views.request_reset, name="request_reset_pswd"),
    path("validate_username", csrf_exempt(views.user_val_view), name="user_val"),
    path("validate_email", csrf_exempt(views.email_val_view), name="email_val"),
    path("activate/<uidb64>/<token>", views.activation_view, name="activate"),
    path("reset/<uidb64>/<token>", views.reset_password, name="reset"),

]
