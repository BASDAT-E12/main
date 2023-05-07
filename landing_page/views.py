from django.shortcuts import render

# Create your views here.
def show_landing_page_manajer(request):
    return render(request, "landing_page_manajer.html")

def show_landing_page_penonton(request):
    return render(request, "landing_page_penonton.html")

def show_landing_page_panitia(request):
    return render(request, "landing_page_panitia.html")
