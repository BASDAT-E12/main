from django.shortcuts import redirect, render
import psycopg2
from django.contrib import messages
import uuid

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

def register(request):
    return render(request, "register.html")

def register_all_roles(request, role):
    print(request.method)
    if request.method == "POST":
        try:
            id = str(uuid.uuid4())

            # print("nyampe sinikah")
            print(role)

            username = request.POST.get("username")
            password = request.POST.get("password")
            nama_depan =request.POST.get("nama_depan")
            nama_belakang = request.POST.get("nama_belakang")
            email = request.POST.get("email")
            no_hp = str(request.POST.get("no_hp"))
            alamat = request.POST.get("alamat")
            status = request.POST.get("status")

            cur.execute("INSERT INTO USER_SYSTEM VALUES(%s, %s)", (username, password))           
            # print("nyampe sinikah??? execute1")
            cur.execute("INSERT INTO NON_PEMAIN VALUES (%s, %s, %s, %s, %s, %s)", (id, nama_depan, nama_belakang, no_hp, email, alamat))
            
            # print("nyampe sinikah??? execute2")

            cur.execute("INSERT INTO STATUS_NON_PEMAIN VALUES (%s,%s)", (id, status))
            # print("nyampe sinikah??? execute3")  

            # print("nyampe sinikah??? execute4")
            if (role == 'manager'):
                cur.execute(" INSERT INTO MANAJER VALUES (%s,%s)", (id, username))
                # print("dia manager loh")

            elif (role == 'penonton'):
                cur.execute(" INSERT INTO PENONTON VALUES (%s,%s)", (id, username))
            elif (role == 'panitia'):
                jabatan = request.POST.get("jabatan")
                cur.execute(" INSERT INTO PANITIA VALUES (%s,%s,%s)", (id, jabatan, username))
            # print("nyampe sinikah??? execute4")
            # print("nyampe sini terakhir")        
        except:
            # print("fail sini")
            if role == 'panitia':
                return render(request, 'register_panitia.html')
            return render(request, 'register_manager_penonton.html')

        finally:
            conn.commit()
            conn.close()
    

def register_penonton(request):
    # context = {'role': 'penonton'}
    # register_all_roles(request, context['role'])
    # return render(request, "register_manager_penonton.html", context)
    if request.method == "POST":
        context = {'role': 'penonton'}
        register_all_roles(request, context['role'])
        return redirect('login_logout:login')
    else:
        context = {'role': 'penonton'}
        return render(request, "register_manager_penonton.html", context)

def register_manager(request):
    # print("masuk managerssss")
    # print(request.method)
    # context = {'role': 'manager'}
    # register_all_roles(request, context['role'])
    # return render(request, "register_manager_penonton.html", context)
    if request.method == "POST":
        context = {'role': 'manager'}
        register_all_roles(request, context['role'])
        return redirect('login_logout:login')
    else:
        context = {'role': 'manager'}
        return render(request, "register_manager_penonton.html", context)

def register_panitia(request):
    context = {'role': 'panitia'}
    # register_all_roles(request, context['role'])
    # return render(request, "register_panitia.html", context)
    if request.method == "POST":
        context = {'role': 'panitia'}
        register_all_roles(request, context['role'])
        return redirect('login_logout:login')
    else:
        context = {'role': 'panitia'}
        return render(request, "register_panitia.html", context)

