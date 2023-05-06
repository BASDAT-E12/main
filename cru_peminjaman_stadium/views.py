from django.shortcuts import render

# Create your views here.
def listpemesanan(request):
    return render(request, "listpemesanan.html")


def listwaktustadium(request):
    return render(request, "listwaktustadium.html")


def peminjamanstadium(request):
    return render(request, "peminjamanstadium.html")