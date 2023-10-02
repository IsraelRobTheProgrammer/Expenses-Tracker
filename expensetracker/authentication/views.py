from django.shortcuts import render
from django.views import View

# Create your views here.


class Register_View(View):
    def get(self, request):
        return render(request, "auth/register.html")


reg_view = Register_View.as_view()
