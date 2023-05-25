from django.shortcuts import render
import psycopg2
from collections import namedtuple

# Create your views here.

DB_NAME = "railway"
DB_HOST = "containers-us-west-63.railway.app"
DB_PASSWORD = "RHLH2Pzmwi6WgL7C2Xhc"
DB_PORT = "6922"
DB_USER = "postgres"

def connection():
    try:
        conn =psycopg2.connect(
            database = DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST,
            port = DB_PORT
        )
        cur = conn.cursor()
        print ("Database connected successfully")
        return conn, cur
    except:
        print ("Database not connected successfully")

def show_history_rapat(request):
    rapat = get_rapat()
    context = {'rapat': rapat}
    return render(request, "history_rapat.html", context)

def show_isi_rapat(request, id):
    conn, cur = connection()
    cur.execute("SELECT isi_rapat FROM RAPAT WHERE id_pertandingan = %s", (id,))
    result = namedtuplefetchall(cur)
    context = {'isi_rapat': result}
    return render(request, "isi_rapat.html", context)

def get_rapat():
    conn, cur = connection()
    cur.execute("SELECT t.id_pertandingan, STRING_AGG(nama_tim, ' VS ') as tim, o.nama_depan || ' ' || o.nama_belakang as nama_panitia, s.nama as nama_stadium, p.start_datetime ||' - '|| p.end_datetime as datetime, r.isi_rapat FROM RAPAT R JOIN PERTANDINGAN P ON R.ID_PERTANDINGAN = P.ID_PERTANDINGAN JOIN STADIUM S ON P.STADIUM = S.ID_STADIUM JOIN TIM_PERTANDINGAN T ON P.ID_PERTANDINGAN = T.ID_PERTANDINGAN JOIN PANITIA N ON N.ID_PANITIA = R.PERWAKILAN_PANITIA JOIN NON_PEMAIN O ON O.ID = N.ID_PANITIA GROUP BY T.id_pertandingan, nama_panitia, s.nama, p.start_datetime, p.end_datetime, r.isi_rapat")
    result = namedtuplefetchall(cur)
    return result 

def namedtuplefetchall(cur):
    """Return all rows from a cursor as a namedtuple"""
    dsc = cur.description
    nt_result = namedtuple('Result', [col[0] for col in dsc]) 
    return [nt_result(*row) for row in cur.fetchall()]
