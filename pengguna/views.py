from django.shortcuts import render

# Create your views here.
def register(request):
    return render(request, "register.html")

def register_manager_penonton(request):
    return render(request, "register_manager_penonton.html")

def register_panitia(request):
    return render(request, "register_panitia.html")