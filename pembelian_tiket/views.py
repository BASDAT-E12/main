from django.shortcuts import render, HttpResponse
import psycopg2
from collections import namedtuple
import random, string

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

def pilih_stadium(request):
    stadium = get_stadium()
    context = {'stadium': stadium}
    try:
        print("hai")
        if request.method == "POST":
            print("ini post")
            return list_pertandingan_tiket(request)
        else:
            print("masuk")
            return render(request, "pilih_stadium.html", context)
    except Exception as e:
        print(e)
        print("salah")

def list_waktu_stadium_tiket(request):
    return render(request, "list_waktu_stadium_tiket.html")

def list_pertandingan_tiket(request):
    if request.method == "POST":
        conn, cur= connection()
        selected_stadium = request.POST.get("stadium")
        date = request.POST.get("date") 
        #f=first group, s=second group
        print(selected_stadium)
        print(date)
        cur.execute("SELECT f.nama, f.start_datetime, f.end_datetime, f.id_pertandingan, f.nama_tim as first_team, s.nama_tim as second_team FROM (SELECT d.nama, p.id_pertandingan, nama_tim, p.start_datetime, p.end_datetime FROM TIM_PERTANDINGAN T JOIN PERTANDINGAN P ON T.ID_PERTANDINGAN = P.ID_PERTANDINGAN JOIN STADIUM D ON D.ID_STADIUM = P.STADIUM) as f JOIN (SELECT d.nama, p.id_pertandingan, nama_tim, p.start_datetime, p.end_datetime FROM TIM_PERTANDINGAN T JOIN PERTANDINGAN P ON T.ID_PERTANDINGAN = P.ID_PERTANDINGAN JOIN STADIUM D ON D.ID_STADIUM = P.STADIUM) as s ON f.id_pertandingan = s.id_pertandingan AND f.start_datetime = s.start_datetime and f.end_datetime = s.end_datetime and f.nama = s.nama where f.nama_tim < s.nama_tim and f.start_datetime <= %s and f.end_datetime >= %s and f.nama=%s", (date, date,selected_stadium))
        result = namedtuplefetchall(cur)
        context = {'stadium': selected_stadium,
                'date':  date,
                'teams': result}
        print(context)
        return render(request, "list_pertandingan_tiket.html", context)
    else:
        return render(request, "list_pertandingan_tiket.html")

def beli_tiket(request, id):
    # try:
        print("hai")
        if request.method == "POST":
            print("ini post")
            conn, cur= connection()
            print("CONNECTION")
            nomor_receipt = ''.join(random.choice(string.ascii_letters) for i in range(10))
            print("RECEIPT")
            kategori = request.POST.get("kategori")
            metode_pembayaran = request.POST.get("metode_pembayaran") 
            print("ini session")
            id_penonton_session = request.session["id_penonton"]
            print("id penonton", id_penonton_session)
            print("gara gara session")
            print(nomor_receipt, kategori, metode_pembayaran, id_penonton_session, id)
            cur.execute("INSERT INTO PEMBELIAN_TIKET VALUES(%s,%s,%s,%s,%s)", (nomor_receipt, id_penonton_session, kategori, metode_pembayaran, id ))  
        else:
            print("masuk")
            return render(request, "beli_tiket.html")
    # except Exception as e:
    #     print(e)
    #     print("salah")
    #     return render(request, "beli_tiket.html")

def get_stadium():
    conn, cur = connection()
    cur.execute("SELECT nama FROM STADIUM")
    result = namedtuplefetchall(cur)
    return result 

def namedtuplefetchall(cur):
    """Return all rows from a cursor as a namedtuple"""
    dsc = cur.description
    nt_result = namedtuple('Result', [col[0] for col in dsc]) 
    return [nt_result(*row) for row in cur.fetchall()]




# SELECT f.date, f.id_pertandingan, f.nama_tim as first_team, s.nama_tim as second_team FROM (SELECT p.id_pertandingan, nama_tim, CONCAT(p.start_datetime, ' - ' ,p.end_datetime) as date FROM TIM_PERTANDINGAN T, PERTANDINGAN P WHERE T.ID_PERTANDINGAN = P.ID_PERTANDINGAN) as f JOIN (SELECT p.id_pertandingan, nama_tim, CONCAT(p.start_datetime, ' - ' ,p.end_datetime) as date FROM TIM_PERTANDINGAN T, PERTANDINGAN P WHERE T.ID_PERTANDINGAN = P.ID_PERTANDINGAN) as s ON f.id_pertandingan = s.id_pertandingan AND f.date = s.date WHERE f.nama_tim < s.nama_tim
