from django.shortcuts import render
import psycopg2
from collections import namedtuple

# Create your views here.
<<<<<<< HEAD
def list_pertandingan_penonton(request):
    return render(request, "list_pertandingan_penonton.html")

def list_pertandingan_manager(request):
    return render(request, "list_pertandingan_manager.html")
=======

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

def list_pertandingan_penonton(request):
    pertandingan = get_pertandingan()
    context = {'pertandingan': pertandingan}
    return render(request, "list_pertandingan_penonton.html", context)

def list_pertandingan_manager(request):
    pertandingan = get_pertandingan()
    context = {'pertandingan': pertandingan}
    return render(request, "list_pertandingan_manager.html", context)

def get_pertandingan():
    cur.execute("SELECT STRING_AGG(nama_tim, ' VS ') as tim, s.nama as nama_stadium, CONCAT(p.start_datetime, ' - ' ,p.end_datetime) as datetime FROM PERTANDINGAN P JOIN STADIUM S ON P.STADIUM = S.ID_STADIUM JOIN TIM_PERTANDINGAN T ON P.ID_PERTANDINGAN = T.ID_PERTANDINGAN GROUP BY T.id_pertandingan, nama_stadium, datetime")
    result = namedtuplefetchall(cur)
    return result 

def namedtuplefetchall(cur):
    """Return all rows from a cursor as a namedtuple"""
    dsc = cur.description
    nt_result = namedtuple('Result', [col[0] for col in dsc]) 
    return [nt_result(*row) for row in cur.fetchall()]

>>>>>>> 3d8f74a49d196fa18e718fda8403587dd6921851
