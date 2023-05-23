from django.shortcuts import render
import psycopg2, psycopg2.extras

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
curr.execute("SELECT * FROM user_system")
rows = curr.fetchone()
print("Username: " + rows[0])
print("Password: " + rows[1])
# for data in rows:
#     print("Nama Tim :" + data[0])
#     print("Universitas :" + data[1])
conn.close()


def show_register_tim(request):
    return render(request, "register_tim.html")

def show_list_tim(request):
    return render(request, "list_tim.html")

def show_register_tim(request):
    return render(request, "register_tim.html")

def show_pilih_pelatih(request):
    return render(request, "pilih_pelatih.html")

def show_pilih_pemain(request):
    return render(request, "pilih_pemain.html")