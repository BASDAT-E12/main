from django.shortcuts import redirect
import psycopg2, psycopg2.extras
from django.http import HttpResponseRedirect

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
    print("Database connected succesfully decorator")
except:
    print("Database not connected successfully")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

def login_required(function):
    def wrapper(request, *args, **kwargs):
        print("function:", function)
        if request is None:
            return HttpResponseRedirect("/login/")
        print(request)
        username = request.session["username"]
        password = request.session["password"]

        if username is None:
            return HttpResponseRedirect("/login/")

        cur.execute(f"""
        SELECT * FROM user_system
        WHERE username='{username}' AND password='{password}'
        """)
        result = cur.fetchall()
        print("result: ", result)
        if result == []:
            return HttpResponseRedirect("/login/")

        return function(request, *args, **kwargs)

    return wrapper