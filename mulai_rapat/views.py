from django.shortcuts import render

# Create your views here.

def choose_match(request):
    return render(request, "pilih_pertandingan.html")

def meeting(request):
    return render(request, "rapat.html")
