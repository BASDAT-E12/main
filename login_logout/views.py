from django.shortcuts import render

# Create your views here.
def formlogin(request):
    return render(request, "formlogin.html")


def login(request):
    return render(request, "login.html")