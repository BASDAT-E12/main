from django.shortcuts import render

# Create your views here.
def grupstageabis(request):
    return render(request, "grupstageabis.html")


def listpertandingan_update(request):
    return render(request, "listpertandingan_update.html")


def listpertandingan(request):
    return render(request, "listpertandingan.html")


def next_belumlengkap(request):
    return render(request, "next_belumlengkap.html")


def next_pertandinganbaru(request):
    return render(request, "next_pertandinganbaru.html")
    
def peristiwatim(request):
    return render(request, "peristiwatim.html")

