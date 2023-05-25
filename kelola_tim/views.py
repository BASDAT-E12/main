from django.shortcuts import render, redirect
import psycopg2, psycopg2.extras
from django.http import HttpResponse
from utils.decorator import login_required

# Create your views here.

DB_NAME = "railway"
DB_HOST = "containers-us-west-63.railway.app"
DB_PASSWORD = "RHLH2Pzmwi6WgL7C2Xhc"
DB_PORT = "6922"
DB_USER = "postgres"

try: 
    conn = psycopg2.connect(
        database = DB_NAME,
        user = DB_USER, 
        password = DB_PASSWORD, 
        host = DB_HOST, 
        port = DB_PORT
    )
    print("Database connected succesfully")
except:
    print("Database not connected successfully")

curr = conn.cursor()
# curr.execute("SELECT * FROM user_system")
# rows = curr.fetchone()
# print("Username: " + rows[0])
# print("Password: " + rows[1])
# for data in rows:
#     print("Nama Tim :" + data[0])
#     print("Universitas :" + data[1])

@login_required
def show_register_tim(request):
    return render(request, "register_tim.html")

@login_required
def show_list_tim(request):
    return render(request, "list_tim.html")

@login_required
def show_register_tim(request):
    return render(request, "register_tim.html")

@login_required
def show_pilih_pelatih(request):
    return render(request, "pilih_pelatih.html")

@login_required
def show_pilih_pemain(request):
    return render(request, "pilih_pemain.html")

@login_required
def get_pemain_tim(nama_tim):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    cur.execute(f"""
    SELECT nama_depan, nama_belakang, nomor_hp, tgl_lahir, is_captain, posisi, npm, jenjang, id_pemain
    FROM pemain
    WHERE nama_tim = '{nama_tim}'""")
    pemain_res = cur.fetchall()
    table_pemain = []
    table_pemain = [
        {
            "nama_pemain": pemain[0] + ' ' + pemain[1],
            "no_hp_pemain" : pemain[2],
            "tgl_lahir_pemain" : pemain[3],
            "is_captain": pemain[4],
            "posisi_pemain": pemain[5],
            "npm": pemain[6], 
            "jenjang_pemain": pemain[7], 
            "id_pemain": pemain[8], 
        }
        for pemain in pemain_res
    ]
    return table_pemain

@login_required
def get_pelatih_tim(nama_tim):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    cur.execute(f"""SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, spesialisasi, id
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
            "id_pelatih": pelatih[6],
        }
        for pelatih in res_pelatih
    ]
    return table_pelatih

@login_required
def manager_check_team(request):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # MANAGER

    cur.execute(f"""SELECT id 
        FROM non_pemain 
        WHERE id in (SELECT id_manajer 
        FROM manajer 
        WHERE username = '{request.session.get('username')}')""")
    user = cur.fetchone()
    id = user[0]
    request.session["id_manajer"] = id

    # CHECK IF MANAGER MANAGE TEAM 
    cur.execute(f"""
    SELECT nama_tim 
    FROM tim_manajer
    WHERE id_manajer = '{id}'""")
    team_result = cur.fetchone()
    try:
        team = team_result[0]
        request.session["nama_tim"] = team
        pemain = get_pemain_tim(team)
        pelatih = get_pelatih_tim(team)
        if(pemain == []):
            pemain = None
        if(pelatih == []):
            pelatih = None
        
        flag = 0
        if(pemain is None and pelatih is None):
            flag = 1
        if(pemain is None and pelatih is not None):
            flag = 2
        if(pemain is not None and pelatih is None):
            flag = 3
        if(pemain is not None and pelatih is not None):
            flag = 4
        context = {
            "nama_tim": team,
            "pemain": pemain, 
            "pelatih": pelatih,  
            "flag": flag
        }
        return render(request, "list_tim.html", context)
    except TypeError:
        return redirect('/kelola_tim/register_tim/')

@login_required
def pilih_pemain_available(request):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # MANAJER
    # cur.execute(f"""SELECT id 
    #     FROM non_pemain 
    #     WHERE id in (SELECT id_manajer 
    #     FROM manajer 
    #     WHERE username = '{request.session.get('username')}')""")
    # user = cur.fetchone()
    # id = user[0]
    id_manajer = request.session["id_manajer"]

    # NAMA TIM 
    # cur.execute(f""" SELECT nama_tim 
    #     FROM tim_manajer
    #     WHERE id_manajer = '{id_manajer}'""")
    # team_result = cur.fetchone()
    # team = team_result[0]

    # PEMAIN AVAILABLE
    cur.execute(f"""
    SELECT nama_depan, nama_belakang, posisi, id_pemain
    FROM pemain 
    WHERE nama_tim IS NULL""")
    pemain_res = cur.fetchall()
    table_pemain = []
    table_pemain = [
        {
            "nama_pemain": pemain[0] + ' ' + pemain[1],
            "posisi_pemain": pemain[2],
            "id_pemain": pemain[3]
        }
        for pemain in pemain_res
    ]
    
    context = {
        "table_pemain": table_pemain, 
        "team": request.session["nama_tim"], 
    }

    return render(request, "pilih_pemain.html", context)

@login_required
def pilih_pelatih_available(request):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # MANAJER
    # cur.execute(f"""SELECT id 
    #     FROM non_pemain 
    #     WHERE id in (SELECT id_manajer 
    #     FROM manajer 
    #     WHERE username = '{request.session.get('username')}')""")
    # user = cur.fetchone()
    # id = user[0]
    id_manajer = request.session["id_manajer"]

    # NAMA TIM 
    cur.execute(f""" SELECT nama_tim 
        FROM tim_manajer
        WHERE id_manajer = '{id_manajer}'""")
    team_result = cur.fetchone()
    team = team_result[0]

    # PELATIH AVAILABLE
    cur.execute(f"""
    SELECT nama_depan, nama_belakang, s.spesialisasi, p.id_pelatih
    FROM pelatih p
    NATURAL JOIN spesialisasi_pelatih s
    JOIN non_pemain n ON p.id_pelatih = n.id
    WHERE p.nama_tim IS NULL; """)
    pelatih_res = cur.fetchall()
    table_pelatih = []
    table_pelatih = [
        {
            "nama_pelatih": pelatih[0] + ' ' + pelatih[1],
            "spesialisasi": pelatih[2],
            "id_pelatih": pelatih[3],
        }
        for pelatih in pelatih_res
    ]
    
    context = {
        "table_pelatih": table_pelatih, 
        "team": request.session["nama_tim"], 
    }
    return render(request, "pilih_pelatih.html", context)

def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg

@login_required
def daftar_pelatih(request):
    if request.method == "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        id_pelatih = request.POST.get("id_pelatih")
        
        # MANAJER
        # cur.execute(f"""SELECT id 
        #     FROM non_pemain 
        #     WHERE id in (SELECT id_manajer 
        #     FROM manajer 
        #     WHERE username = '{request.session.get('username')}')""")
        # user = cur.fetchone()
        id_manajer = request.session["id_manajer"]

        # NAMA TIM 
        # cur.execute(f""" SELECT nama_tim 
        #     FROM tim_manajer
        #     WHERE id_manajer = '{id_manajer}'""")
        # team_result = cur.fetchone()
        # team = team_result[0]
        nama_tim = request.session["nama_tim"]
        
        try:
            cur.execute(f"""UPDATE pelatih
            SET nama_tim = '{nama_tim}'
            WHERE id_pelatih = '{id_pelatih}'""")
            conn.commit()

            cur.execute(f"""
            SELECT nama_tim 
            FROM tim_manajer
            WHERE id_manajer = '{id_manajer}'""")
            team_result = cur.fetchone()
            team = team_result[0]
            pemain = get_pemain_tim(nama_tim)
            pelatih = get_pelatih_tim(nama_tim)
            context = {
                "nama_tim": nama_tim,
                "pemain": pemain, 
                "pelatih": pelatih,  
            }
            return redirect('kelola_tim:manager_check_team')
        except Exception as e:
            conn.rollback()
            message = {
                "message": generate_error_message(e), 
                "error_flag": True, 
            }
            
            return render(request, "pilih_pelatih.html", message)

@login_required
def daftar_pemain(request):
     if request.method == "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        id_pemain = request.POST.get("id_pemain")

        # MANAJER
        cur.execute(f"""SELECT id 
            FROM non_pemain 
            WHERE id in (SELECT id_manajer 
            FROM manajer 
            WHERE username = '{request.session.get('username')}')""")
        user = cur.fetchone()
        id_manajer = request.session["id_manajer"]

        # NAMA TIM 
        cur.execute(f""" SELECT nama_tim 
            FROM tim_manajer
            WHERE id_manajer = '{id_manajer}'""")
        team_result = cur.fetchone()
        team = team_result[0]
        nama_tim = request.session["nama_tim"]

        cur.execute(f"""UPDATE pemain
        SET nama_tim = '{nama_tim}'
        WHERE id_pemain = '{id_pemain}'""")
        conn.commit()

        # cur.execute(f"""
        # SELECT nama_tim 
        # FROM tim_manajer
        # WHERE id_manajer = '{id_manajer}'""")
        # team_result = cur.fetchone()
        # team = team_result[0]

        pemain = get_pemain_tim(nama_tim)
        pelatih = get_pelatih_tim(nama_tim)
        context = {
            "nama_tim": nama_tim,
            "pemain": pemain, 
            "pelatih": pelatih,  
        }
        return redirect('kelola_tim:manager_check_team')
        #return render(request, "list_tim.html", context)

@login_required
def delete_pelatih(request, id):
    if request.method == "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        id_pelatih = id
        # MANAJER
        cur.execute(f"""SELECT id 
            FROM non_pemain 
            WHERE id in (SELECT id_manajer 
            FROM manajer 
            WHERE username = '{request.session.get('username')}')""")
        user = cur.fetchone()
        id_manajer = request.session["id_manajer"]

        # NAMA TIM 
        cur.execute(f""" SELECT nama_tim 
            FROM tim_manajer
            WHERE id_manajer = '{id_manajer}'""")
        team_result = cur.fetchone()
        team = team_result[0]
        nama_tim = request.session["nama_tim"]

        cur.execute(f"""UPDATE pelatih
        SET nama_tim = NULL
        WHERE id_pelatih = '{id_pelatih}'""")
        conn.commit()

        # cur.execute(f"""
        # SELECT nama_tim 
        # FROM tim_manajer
        # WHERE id_manajer = '{id_manajer}'""")
        # team_result = cur.fetchone()
        # team = team_result[0]

        pemain = get_pemain_tim(nama_tim)
        pelatih = get_pelatih_tim(nama_tim)
        context = {
            "nama_tim": nama_tim,
            "pemain": pemain, 
            "pelatih": pelatih,  
        }
        return redirect('kelola_tim:manager_check_team')
        #return render(request, "list_tim.html", context)

@login_required
def delete_pemain(request, id):
    # if request.method == "POST":
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_pemain = id

    # MANAJER
    # cur.execute(f"""SELECT id 
    #     FROM non_pemain 
    #     WHERE id in (SELECT id_manajer 
    #     FROM manajer 
    #     WHERE username = '{request.session.get('username')}')""")
    # user = cur.fetchone()
    # id_manajer = user[0]

    # NAMA TIM 
    cur.execute(f""" SELECT nama_tim 
        FROM tim_manajer
        WHERE id_manajer = '{request.session["id_manajer"]}'""")
    team_result = cur.fetchone()
    team = team_result[0]
    nama_tim = request.session["nama_tim"]

    cur.execute(f"""UPDATE pemain
    SET nama_tim = NULL
    WHERE id_pemain = '{id_pemain}'""")
    conn.commit()

    # cur.execute(f"""
    # SELECT nama_tim 
    # FROM tim_manajer
    # WHERE id_manajer = '{request.session["id_manajer"]}'""")
    # team_result = cur.fetchone()
    # team = team_result[0]

    pemain = get_pemain_tim(nama_tim)
    pelatih = get_pelatih_tim(nama_tim)
    context = {
        "nama_tim": nama_tim,
        "pemain": pemain, 
        "pelatih": pelatih,  
    }
    return redirect('kelola_tim:manager_check_team')
    #return render(request, "list_tim.html", context)

@login_required
def make_captain(request, id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_pemain = id

    cur.execute(f"""UPDATE pemain
        SET is_captain = TRUE
        WHERE id_pemain = '{id_pemain}'""")
    conn.commit()

    return redirect('kelola_tim:manager_check_team')

@login_required
def create_tim(request):
    if request.method == "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        nama_tim = request.POST.get('nama_tim')
        print(nama_tim)
        nama_univ = request.POST.get('nama_univ')
        print(nama_univ)
        try: 
            print("masuk")
            cur.execute(f"""INSERT INTO tim VALUES
            ('{nama_tim}', '{nama_univ}')
            """)

            # MANAJER
            # cur.execute(f"""SELECT id 
            #     FROM non_pemain 
            #     WHERE id in (SELECT id_manajer 
            #     FROM manajer 
            #     WHERE username = '{request.session.get('username')}')""")
            # user = cur.fetchone()
            # #id_manajer = user[0]
            id_manajer = request.session["id_manajer"]

            cur.execute(f"""INSERT INTO tim_manajer VALUES
            ('{id_manajer}', '{nama_tim}')""")
            conn.commit()
            return redirect('kelola_tim:manager_check_team')
        except Exception as e:
            conn.rollback()
            return HttpResponse(e)

        

