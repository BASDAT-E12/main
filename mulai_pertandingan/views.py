from django.shortcuts import render

# Create your views here.

def start_match(request):
    return render(request, "mulai_pertandingan.html")

def choose_episode(request):
    return render(request, "pilih_peristiwa.html")