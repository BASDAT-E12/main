from django.shortcuts import render

# Create your views here.
def list_pertandingan_penonton_manager(request):
    return render(request, "list_pertandingan_penonton_manager.html")
