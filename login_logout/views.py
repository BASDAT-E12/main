from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import connection
import psycopg2


# Create your views here.
# CONNECT TO DB
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

def formlogin(request):
    return render(request, "formlogin.html")

def login(request):
    return render(request, "login.html")

def authenticate(request):
    
    cursor = conn.cursor()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # CHECK IF USER EXISTS 
        try: 
            cursor.execute("SELECT * FROM user_system WHERE username = %s AND password = %s",  (username, password, ))
        except Exception as e:
            cursor = conn.cursor()
        result = cursor.fetchone()
        if result is not None:
            request.session["username"] = result[0]
            request.session["password"] = result[1]
            request.session["is_authenticated"] = True
            request.session["is_verified"] = result[0] is not None #blm tau bener apa ga
            # DETERMINE ROLE 
            
            # MANAJER
            try:
                cursor.execute("SELECT * FROM manajer WHERE username = %s",  [username,])
            except Exception as e:
                cursor = conn.cursor()
            result = cursor.fetchone()
            if result is not None:
                request.session["role"] = "manajer"
                request.session["id_manajer"] = result[0]
                return redirect("landing_page:index") 
            
            # PANITIA
            try:
                cursor.execute("SELECT * FROM panitia WHERE username = %s", [username,])
            except Exception as e:
                cursor = conn.cursor()
            result = cursor.fetchone()
            if result is not None:
                request.session["role"] = "panitia"
                request.session["id_panitia"] = result[0]
                return redirect("landing_page:index") 

            # PENONTON
            try:
                cursor.execute("SELECT * FROM penonton WHERE username = %s", [username,])
            except Exception as e:
                cursor = conn.cursor()
            result = cursor.fetchone()
            if result is not None:
                request.session["role"] = "penonton"
                request.session["id_penonton"] = result[0]
                print("id_penonton: ", request.session["id_penonton"])
                return redirect("landing_page:index")
    else: 
        #Username atau password salah 
        print("Username atau password salah")
    #cursor.close()
    return render(request, "formlogin.html")

def logout(request):
    request.session.flush()
    return redirect("login")



