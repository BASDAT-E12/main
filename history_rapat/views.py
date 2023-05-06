from django.shortcuts import render

# Create your views here.
def show_history_rapat(request):
    return render(request, "history_rapat.html")
