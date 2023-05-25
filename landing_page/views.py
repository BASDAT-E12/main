from django.shortcuts import render
import psycopg2, psycopg2.extras
from django.db import connection
from utils.decorator import login_required
import json 
# Create your views here.
# CONNECT TO DB
DB_NAME = "railway"
DB_HOST = "containers-us-west-63.railway.app"
DB_PASSWORD = "RHLH2Pzmwi6WgL7C2Xhc"
DB_PORT = "6922"
DB_USER = "postgres"

# try: 
#     conn = psycopg2.connect(
#         database = DB_NAME,
#         user = DB_USER, 
#         password = DB_PASSWORD, 
#         host = DB_HOST, 
#         port = DB_PORT
#     )
#     print("Database connected succesfully")
        
# except:
#     print("Database not connected successfully")

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

# @login_required
def find_manajer(str):
    conn, cur = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT concat(nama_depan, ' ', nama_belakang) FROM non_pemain WHERE id = '{str}'")
    result = cur.fetchone()
    return result[0]

# @login_required
def find_status(id_non_pemain):
    conn, cur = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT status FROM status_non_pemain WHERE id_non_pemain = '{id_non_pemain}'")
    result = cur.fetchone()
    return result[0]

# @login_required
def get_role(request):
    conn, cur = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    role = request.session.get("role", None)
    
    # MANAJER
    if role == "manajer":
        print("id manajer here: ", request.session["id_manajer"])
        
        cur.execute(f"""SELECT * 
        FROM non_pemain 
        WHERE id in (SELECT id_manajer 
        FROM manajer 
        WHERE username = '{request.session.get('username')}')""")
        result = cur.fetchone()
        id = result[0]
        nama_depan = result[1]
        nama_belakang = result[2]
        nomor_hp = result[3]
        email = result[4]
        alamat = result[5]
        status = find_status(id)

        cur.execute(f"""SELECT nama_tim 
        FROM tim_manajer 
        WHERE id_manajer = '{id}'""")
        result = cur.fetchone() 
        check_tim = True
        try:
            nama_tim = result[0]
        except TypeError as e:
            
            if(result is None):
                check_tim = False
                context = {
                "id": id, 
                "nama_depan": nama_depan, 
                "nama_belakang": nama_belakang, 
                "nomor_hp": nomor_hp, 
                "email": email, 
                "alamat": alamat, 
                "status": status, 
                "check_tim": check_tim, 
                }
            return show_landing_page_manajer(request, context)
        
        # MENAMPILKAN DATA TIM (PEMAIN)
        
        cur.execute(f"SELECT * FROM pemain WHERE nama_tim = '{nama_tim}'")
        result_pemain = cur.fetchall()
        table_pemain = []
        table_pemain = [
            {
                "nama_pemain": pemain[2] + ' ' + pemain[3],
                "no_hp_pemain" : pemain[4],
                "tgl_lahir_pemain" : pemain[5],
                "is_captain": pemain[6],
                "posisi_pemain": pemain[7],
                "npm": pemain[8], 
                "jenjang_pemain": pemain[9], 
            }
            for pemain in result_pemain
        ]
        
        # MENAMPILKAN DATA TIM (PELATIH)

        # ID PELATIH
        cur.execute(f"""SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, spesialisasi
        FROM non_pemain 
        JOIN spesialisasi_pelatih ON non_pemain.id = spesialisasi_pelatih.id_pelatih
        WHERE id IN (SELECT id_pelatih from PELATIH WHERE nama_tim = '{nama_tim}')
        """)
        res_pelatih = cur.fetchall()
        table_pelatih = []
        table_pelatih = [
            {
                "nama_pelatih": pelatih[0] + ' ' + pelatih[1],
                "nomor_hp": pelatih[2], 
                "email": pelatih[3],
                "alamat": pelatih[4],
                "spesialisasi": pelatih[5], 
            }
            for pelatih in res_pelatih
        ]

        if(table_pemain == []):
            table_pemain = None
        if(table_pelatih == []):
            table_pelatih = None
        
        flag = 0
        if(table_pemain is None and table_pelatih is None):
            flag = 1
        if(table_pemain is None and table_pelatih is not None):
            flag = 2
        if(table_pemain is not None and table_pelatih is None):
            flag = 3
        if(table_pemain is not None and table_pelatih is not None):
            flag = 4

        context = {
            "id": id, 
            "nama_depan": nama_depan, 
            "nama_belakang": nama_belakang, 
            "nomor_hp": nomor_hp, 
            "email": email, 
            "alamat": alamat, 
            "status": status, 
            "table_pemain": table_pemain, 
            "table_pelatih": table_pelatih,
            "table_pemain": table_pemain,
            "nama_tim": nama_tim, 
            "check_tim": check_tim, 
            "flag": flag
        }

        return show_landing_page_manajer(request, context)

    # PANITIA
    elif role == "panitia": 
        cur.execute(f"""SELECT * 
        FROM non_pemain 
        WHERE id in (SELECT id_panitia 
        FROM panitia 
        WHERE username = '{request.session.get('username')}');""")
        result = cur.fetchone()
        id = result[0]
        nama_depan = result[1]
        nama_belakang = result[2]
        nomor_hp = result[3]
        email = result[4]
        alamat = result[5]
        status = find_status(id)


        cur.execute(f"""
        SELECT jabatan
        FROM panitia
        WHERE id_panitia = '{id}'""")

        jabatan = cur.fetchone()[0]

        cur.execute(f"""
        SELECT id_pertandingan, string_agg(nama_tim, ' vs '), manajer_tim_a, manajer_tim_b, datetime, perwakilan_panitia
        FROM rapat 
        NATURAL JOIN tim_pertandingan
        WHERE perwakilan_panitia = '{id}'
        GROUP BY id_pertandingan, manajer_tim_a, manajer_tim_b, datetime, perwakilan_panitia
        """)
        result_rapat = cur.fetchall()
        table_rapat = []
        if (result_rapat == []): 
            context = {
                "id": id, 
                "nama_depan": nama_depan, 
                "nama_belakang": nama_belakang, 
                "nomor_hp": nomor_hp, 
                "email": email, 
                "alamat": alamat, 
                "status": status, 
                "jabatan": jabatan,
                "check_rapat": None, 
            }
            return render(request, "landing_page_panitia.html", context)  
        else:
           table_rapat = [
                {
                    "id_pertandingan": r[0],
                    "tim_bertanding" : r[1], 
                    "manajer_tim_a": find_manajer(r[2]),
                    "manajer_tim_b": find_manajer(r[3]), 
                    "tgl_rapat": r[4], 
                }
                for r in result_rapat
            ]
        
        context = {
            "id": id, 
            "nama_depan": nama_depan, 
            "nama_belakang": nama_belakang, 
            "nomor_hp": nomor_hp, 
            "email": email, 
            "alamat": alamat, 
            "status": status, 
            "jabatan": jabatan,
            "table_rapat": table_rapat, 
            "result_rapat": result_rapat, 
            "check_rapat": "isi", 
        }
        return render(request, "landing_page_panitia.html", context)
    
    # PENONTON 
    elif role == "penonton":
        cur.execute(f"""SELECT * 
        FROM non_pemain 
        WHERE id in (SELECT id_penonton
        FROM penonton
        WHERE username = '{request.session.get('username')}')""")
        result = cur.fetchone()
        id = result[0]
        nama_depan = result[1]
        nama_belakang = result[2]
        nomor_hp = result[3]
        email = result[4]
        alamat = result[5]
        status = find_status(id)


        cur.execute(f"""
        SELECT id_pertandingan, string_agg(nama_tim, ' vs '), stadium, start_datetime, end_datetime, jenis_tiket
        FROM pertandingan
        NATURAL JOIN tim_pertandingan
        NATURAL JOIN pembelian_tiket
        WHERE id_penonton = '{id}'
        GROUP BY id_pertandingan, stadium, start_datetime, end_datetime, jenis_tiket;""")
        
        result_pertandingan = cur.fetchall()
        ada_pertandingan = True

        if(result_pertandingan == []):
            ada_pertandingan = False
            context = {
            "id": id, 
            "nama_depan": nama_depan, 
            "nama_belakang": nama_belakang, 
            "nomor_hp": nomor_hp, 
            "email": email, 
            "alamat": alamat, 
            "status": status, 
            "ada_pertandingan": ada_pertandingan, 
            }
            return render(request, "landing_page_penonton.html", context)
        
        cur.execute(f"""SELECT nama FROM stadium WHERE id_stadium 
        IN (SELECT stadium 
        FROM pertandingan
        NATURAL JOIN tim_pertandingan
        NATURAL JOIN pembelian_tiket
        WHERE id_penonton = '{id}')""")
        nama_stadium = cur.fetchone()
        table_pertandingan = []
        table_pertandingan = [
            {
            'id_pertandingan': p[0],
            'tim_pertandingan': p[1],
            'stadium': nama_stadium[0], 
            'start_datetime': p[3], 
            'end_datetime': p[4],
            'jenis_tiket': p[5], 
            }
            for p in result_pertandingan
        ]

        context = {
            "id": id, 
            "nama_depan": nama_depan, 
            "nama_belakang": nama_belakang, 
            "nomor_hp": nomor_hp, 
            "email": email, 
            "alamat": alamat, 
            "status": status, 
            "table_pertandingan": table_pertandingan, 
            "ada_pertandingan": "Ada", 
        }
        return render(request, "landing_page_penonton.html", context)
    cur.close()
    return render(request, "formlogin.html")

# @login_required
def show_landing_page_manajer(request, context):
    return render(request, "landing_page_manajer.html", context)

# @login_required
def back_landing_page_manajer(request):
    return render(request, "landing_page_manajer.html")

# @login_required
def show_landing_page_penonton(request):
    return render(request, "landing_page_penonton.html")

# @login_required
def show_landing_page_panitia(request):
    return render(request, "landing_page_panitia.html")


