from django.shortcuts import render

# Create your views here.
def show_list_pertandingan(request):
    return render(request, "list_pertandingan.html")


def choose_stadium(request):
    return render(request, "memilih_stadium.html")


def choose_time(request):
    return render(request, "memilih_waktu.html")


def create_match(request):
    return render(request, "buat_pertandingan.html")
