from django.shortcuts import render
import psycopg2
from collections import namedtuple

# Create your views here.
DB_NAME = "railway"
DB_HOST = "containers-us-west-63.railway.app"
DB_PASSWORD = "RHLH2Pzmwi6WgL7C2Xhc"
DB_PORT = "6922"
DB_USER = "postgres"

try:
    conn =psycopg2.connect(
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )
    print ("Database connected successfully")
except:
    print ("Database not connected successfully")

cur = conn.cursor()

def pilih_stadium(request):
    try:
        if request.method == "POST":
            print("ini post")
            try:
                stadium = request.POST.get("stadium")
                date = request.POST.get("date") 
                context = {'stadium': stadium,
                           'date':  date}
                return render(request, "list_waktu_stadium_tiket.html", context)
            finally:
                conn.commit()
                conn.close()
        else:
            print("masuk")
            stadium = get_stadium()
            context = {'stadium': stadium}
            return render(request, "pilih_stadium.html", context)
    except:
        print("salah")


def list_waktu_stadium_tiket(request):
    return render(request, "list_waktu_stadium_tiket.html")

def list_pertandingan_tiket(request):
    return render(request, "list_pertandingan_tiket.html")

def beli_tiket(request):
    return render(request, "beli_tiket.html")

def get_stadium():
    cur.execute("SELECT nama FROM STADIUM")
    result = namedtuplefetchall(cur)
    return result 

def namedtuplefetchall(cur):
    """Return all rows from a cursor as a namedtuple"""
    dsc = cur.description
    nt_result = namedtuple('Result', [col[0] for col in dsc]) 
    return [nt_result(*row) for row in cur.fetchall()]


