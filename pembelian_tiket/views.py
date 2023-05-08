from django.shortcuts import render

# Create your views here.
def pilih_stadium(request):
    return render(request, "pilih_stadium.html")

def list_waktu_stadium_tiket(request):
    return render(request, "list_waktu_stadium_tiket.html")

def list_pertandingan_tiket(request):
    return render(request, "list_pertandingan_tiket.html")

def beli_tiket(request):
    return render(request, "beli_tiket.html")

