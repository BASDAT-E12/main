from django.shortcuts import render
from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse

from django.urls import reverse
import json
import json
from django.shortcuts import render
from django.http import JsonResponse
from uuid import UUID

import datetime
import uuid


# Create your views here.


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



def get_id_panitia_loggedIn(request):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    role = request.session.get("role", None)
    
    if role == "panitia": 
        cur.execute(f"""SELECT * 
        FROM non_pemain 
        WHERE id in (SELECT id_panitia 
        FROM panitia 
        WHERE username = '{request.session.get('username')}');""")
        result = cur.fetchone()
        id = result[0]
        return id


def show_list_pertandingan(request):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_panitia = get_id_panitia_loggedIn(request)
    cur.execute(f"""
    SELECT tm.id_pertandingan, STRING_AGG(tm.nama_tim, ' vs ') AS tim_bertanding
    FROM TIM_PERTANDINGAN AS tm
    GROUP BY tm.id_pertandingan;
    """)
    list_pertandingan = cur.fetchall()
    list_pertandingan_dict = {}
    for row in list_pertandingan:
        list_pertandingan_dict[row['id_pertandingan']] = row['tim_bertanding']

    context = {
        "id_panitia": id_panitia,
        "list_pertandingan": list_pertandingan_dict
    }
    return render(request, "list_pertandingan.html", context)


def choose_time(request, stadium_name):
    if stadium_name == '__stadium_name__':
        stadium_name = request.GET.get('stadium_name', '')
        

    # Generate a list of time slots with a 2-hour gap

    date_value = request.session["date_value"]
    print(request.session["date_value"])
    stadium_name = request.GET.get('stadium_name')
    request.session["stadium_name"] = stadium_name
    start_hour = 0
    end_hour = 23
    time_slots = []
    while start_hour <= end_hour:
        time_slot = f"{start_hour:02}:00 - {start_hour+2:02}:00"
        time_slots.append(time_slot)
        start_hour += 2

    context = {
        'hours': time_slots,
        'stadium_name': stadium_name,
        'date_value': date_value,
    }

    return render(request, 'memilih_waktu.html', context)

def submit_match(request):
    if request.method == "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        wasit_utama = request.POST.get('wasitUtama')
        wasit_Pembantu1 = request.POST.get('wasitPembantu1')
        wasit_Pembantu2 = request.POST.get('wasitPembantu2')
        wasit_Cadangan = request.POST.get('wasitCadangan')
        tim1 = request.POST.get('tim1')
        tim2 = request.POST.get('tim2')



        # Convert start date to datetime with the desired format
        date_value = request.session["date_value"]
        start_datetime = datetime.datetime.strptime(date_value, "%Y-%m-%d")

# Calculate end datetime as 2 hours from start datetime
        end_datetime = start_datetime + datetime.timedelta(hours=2)

# Convert end datetime to string with the desired format
        end_datetime = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Convert start datetime to string with the desired format
        start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M:%S")



        # Retrieve referee IDs and positions
        referees = [
            (wasit_utama, 'Wasit Utama'),
            (wasit_Pembantu1, 'Wasit Pembantu 1'),
            (wasit_Pembantu2, 'Wasit Pembantu 2'),
            (wasit_Cadangan, 'Wasit Cadangan')
        ]

        referee_ids = []
        for referee_name, referee_position in referees:
            if not referee_name:
        # Handle the case when the referee name is empty
                raise Exception("Referee name cannot be empty")
            cur.execute("""
            SELECT w.id_wasit
            FROM WASIT w
            JOIN NON_PEMAIN np ON np.id = w.id_wasit
            WHERE CONCAT(np.nama_depan, ' ', np.nama_belakang) = %s
            """, (referee_name,))
            referee_row = cur.fetchone()
            if referee_row is None:
                # Handle the case when the referee is not found
                raise Exception(f"Referee '{referee_name}' not found")
            referee_id = referee_row['id_wasit']
            referee_ids.append((referee_id, referee_position,))

       

        stadium_name = request.session["stadium_name"]

        print(stadium_name)

        # Retrieve stadium ID
        cur.execute("""
        SELECT id_stadium
        FROM STADIUM
        WHERE nama = %s;
        """, (stadium_name,))
        stadium_id = cur.fetchone()['id_stadium']


        # Insert into PERTANDINGAN table
        pertandingan_id = uuid.uuid4()  # Generate a new UUID for pertandingan



        cur.execute("""
        INSERT INTO PERTANDINGAN (id_pertandingan, start_datetime, end_datetime, stadium)
        VALUES (%s, %s, %s, %s)
        """, (str(pertandingan_id), start_datetime, end_datetime, stadium_id,))

        # Insert into WASIT_BERTUGAS table
        for referee_id, referee_position in referee_ids:
            cur.execute("""
            INSERT INTO WASIT_BERTUGAS (id_wasit, id_pertandingan, posisi_wasit)
            VALUES (%s, %s, %s)
            """, (referee_id, str(pertandingan_id), referee_position,))

        # # Insert into TIM_PERTANDINGAN table
        # cur.execute("""
        # INSERT INTO TIM_PERTANDINGAN (nama_tim, id_pertandingan, skor)
        # VALUES (%s, %s, %s), (%s, %s, %s)
        # """, (tim1, str(pertandingan_id), '0', tim2, str(pertandingan_id), '0',))


        cur.execute("""
        INSERT INTO TIM_PERTANDINGAN (nama_tim, id_pertandingan, skor)
        VALUES (%s, %s, %s)
        """, (tim1, str(pertandingan_id), '0',))

        cur.execute("""
        INSERT INTO TIM_PERTANDINGAN (nama_tim, id_pertandingan, skor)
        VALUES (%s, %s, %s)
        """, (tim2, str(pertandingan_id), '0',))

        # Commit the changes
        conn.commit()

        # Close the cursor
        cur.close()

        

        return redirect('membuat_pertandingan:show_list_pertandingan')
    

def update_pertandingan(request, id_pertandingan):
    if request.method == "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        wasit_utama = request.POST.get('wasitUtama')
        wasit_pembantu1 = request.POST.get('wasitPembantu1')
        wasit_pembantu2 = request.POST.get('wasitPembantu2')
        wasit_cadangan = request.POST.get('wasitCadangan')
        tim1 = request.POST.get('tim1')
        tim2 = request.POST.get('tim2')

        # Convert start date to datetime with the desired format
        date_value = request.session["date_value"]
        start_datetime = datetime.datetime.strptime(date_value, "%Y-%m-%d")

        # Calculate end datetime as 2 hours from start datetime
        end_datetime = start_datetime + datetime.timedelta(hours=2)

        # Convert end datetime to string with the desired format
        end_datetime = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Convert start datetime to string with the desired format
        start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve referee IDs and positions
        referees = [
            (wasit_utama, 'Wasit Utama'),
            (wasit_pembantu1, 'Wasit Pembantu 1'),
            (wasit_pembantu2, 'Wasit Pembantu 2'),
            (wasit_cadangan, 'Wasit Cadangan')
        ]

        referee_ids = []
        for referee_name, referee_position in referees:
            if not referee_name:
                # Handle the case when the referee name is empty
                raise Exception("Referee name cannot be empty")
            cur.execute("""
            SELECT w.id_wasit
            FROM WASIT w
            JOIN NON_PEMAIN np ON np.id = w.id_wasit
            WHERE CONCAT(np.nama_depan, ' ', np.nama_belakang) = %s
            """, (referee_name,))
            referee_row = cur.fetchone()
            if referee_row is None:
                # Handle the case when the referee is not found
                raise Exception(f"Referee '{referee_name}' not found")
            referee_id = referee_row['id_wasit']
            referee_ids.append((referee_id, referee_position))

        stadium_name = request.session["stadium_name"]

        # Retrieve stadium ID
        cur.execute("""
        SELECT id_stadium
        FROM STADIUM
        WHERE nama = %s;
        """, (stadium_name,))
        stadium_id = cur.fetchone()['id_stadium']

        # Update PERTANDINGAN table
        cur.execute("""
        UPDATE PERTANDINGAN
        SET start_datetime = %s, end_datetime = %s, stadium = %s
        WHERE id_pertandingan = %s
        """, (start_datetime, end_datetime, stadium_id, id_pertandingan))

        # Update WASIT_BERTUGAS table
        cur.execute("""
        DELETE FROM WASIT_BERTUGAS
        WHERE id_pertandingan = %s
        """, (id_pertandingan,))
        for referee_id, referee_position in referee_ids:
            cur.execute("""
            INSERT INTO WASIT_BERTUGAS (id_wasit, id_pertandingan, posisi_wasit)
            VALUES (%s, %s, %s)
            """, (referee_id, id_pertandingan, referee_position))

        # Update TIM_PERTANDINGAN table
        cur.execute("""
        DELETE FROM TIM_PERTANDINGAN
        WHERE id_pertandingan = %s
        """, (id_pertandingan,))
        cur.execute("""
        INSERT INTO TIM_PERTANDINGAN (nama_tim, id_pertandingan, skor)
        VALUES (%s, %s, %s), (%s, %s, %s)
        """, (tim1, id_pertandingan, '0', tim2, id_pertandingan, '0'))

        # Commit the changes
        conn.commit()

        # Close the cursor
        cur.close()

        return redirect('membuat_pertandingan:show_list_pertandingan')



def create_match(request):
    # if request.method == "POST":
        # Process the form data
    print("test")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_panitia = get_id_panitia_loggedIn(request)


    date_value = request.session["date_value"]
    print(request.session["date_value"])


    stadium_name = request.session["stadium_name"]
    print(request.session["stadium_name"])

    print(stadium_name)


    cur.execute("""
    SELECT w.id_wasit, np.nama_depan, np.nama_belakang
    FROM WASIT w
    LEFT JOIN NON_PEMAIN np ON w.id_wasit = np.id
    WHERE w.id_wasit NOT IN (
        SELECT wb.id_wasit
        FROM WASIT_BERTUGAS wb
        INNER JOIN PERTANDINGAN p ON wb.id_pertandingan = p.id_pertandingan
        WHERE DATE(p.start_datetime) = %s
    )
    GROUP BY w.id_wasit, np.nama_depan, np.nama_belakang;
    """, (date_value,))

    wasit_list = [row['nama_depan'] + ' ' + row['nama_belakang'] for row in cur.fetchall()]  # Store the referee names in a list


    cur.execute("""
    SELECT T.nama_tim
    FROM TIM AS T
    WHERE T.nama_tim NOT IN (
        SELECT TP.nama_tim
        FROM TIM_PERTANDINGAN AS TP
        INNER JOIN PERTANDINGAN AS P ON TP.id_pertandingan = P.id_pertandingan
        WHERE DATE(%s) BETWEEN P.start_datetime::date AND P.end_datetime::date
    );
    """, (date_value,))

    team_list = [row['nama_tim'] for row in cur.fetchall()]  # Store the team names in a list

    context = {
        "id_panitia": id_panitia,
        "wasit_list": wasit_list,  # Include the referee names in the context as a list
        "team_list": team_list,  # Include the team names in the context as a list
        "date": date_value,
        "date_value": date_value,  # Add the date_value to the context
        "stadium_name":stadium_name
    }

    return render(request, "membuat_pertandingan.html", context)


def update_create_match(request):
    # if request.method == "POST":
        # Process the form data
    print("test")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_panitia = get_id_panitia_loggedIn(request)


    date_value = request.session["date_value"]
    print(request.session["date_value"])


    stadium_name = request.session["stadium_name"]
    print(request.session["stadium_name"])

    print(stadium_name)


    cur.execute("""
    SELECT w.id_wasit, np.nama_depan, np.nama_belakang
    FROM WASIT w
    LEFT JOIN NON_PEMAIN np ON w.id_wasit = np.id
    WHERE w.id_wasit NOT IN (
        SELECT wb.id_wasit
        FROM WASIT_BERTUGAS wb
        INNER JOIN PERTANDINGAN p ON wb.id_pertandingan = p.id_pertandingan
        WHERE DATE(p.start_datetime) = %s
    )
    GROUP BY w.id_wasit, np.nama_depan, np.nama_belakang;
    """, (date_value,))

    wasit_list = [row['nama_depan'] + ' ' + row['nama_belakang'] for row in cur.fetchall()]  # Store the referee names in a list


    cur.execute("""
    SELECT T.nama_tim
    FROM TIM AS T
    WHERE T.nama_tim NOT IN (
        SELECT TP.nama_tim
        FROM TIM_PERTANDINGAN AS TP
        INNER JOIN PERTANDINGAN AS P ON TP.id_pertandingan = P.id_pertandingan
        WHERE DATE(%s) BETWEEN P.start_datetime::date AND P.end_datetime::date
    );
    """, (date_value,))

    team_list = [row['nama_tim'] for row in cur.fetchall()]  # Store the team names in a list

    context = {
        "id_panitia": id_panitia,
        "wasit_list": wasit_list,  # Include the referee names in the context as a list
        "team_list": team_list,  # Include the team names in the context as a list
        "date": date_value,
        "date_value": date_value,  # Add the date_value to the context
        "stadium_name":stadium_name
    }

    return render(request, "update_membuat_pertandingan.html", context)


def delete_pertandingan(request, id_pertandingan):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_panitia = get_id_panitia_loggedIn(request)
    id_pertandingan_str = str(id_pertandingan)  # Convert UUID to string
    cur.execute("DELETE FROM PERTANDINGAN WHERE id_pertandingan = %s", (id_pertandingan_str,))
    conn.commit()
    return HttpResponseRedirect(reverse('membuat_pertandingan:show_list_pertandingan'))


def update_submit_match(request, id_pertandingan):
    if request.method == "POST":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        wasit_utama = request.POST.get('wasitUtama')
        wasit_pembantu1 = request.POST.get('wasitPembantu1')
        wasit_pembantu2 = request.POST.get('wasitPembantu2')
        wasit_cadangan = request.POST.get('wasitCadangan')
        tim1 = request.POST.get('tim1')
        tim2 = request.POST.get('tim2')

        # Convert start date to datetime with the desired format
        date_value = request.session["date_value"]
        start_datetime = datetime.datetime.strptime(date_value, "%Y-%m-%d")

        # Calculate end datetime as 2 hours from start datetime
        end_datetime = start_datetime + datetime.timedelta(hours=2)

        # Convert end datetime to string with the desired format
        end_datetime = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Convert start datetime to string with the desired format
        start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve referee IDs and positions
        referees = [
            (wasit_utama, 'Wasit Utama'),
            (wasit_pembantu1, 'Wasit Pembantu 1'),
            (wasit_pembantu2, 'Wasit Pembantu 2'),
            (wasit_cadangan, 'Wasit Cadangan')
        ]

        referee_ids = []
        for referee_name, referee_position in referees:
            if not referee_name:
                # Handle the case when the referee name is empty
                raise Exception("Referee name cannot be empty")
            cur.execute("""
            SELECT w.id_wasit
            FROM WASIT w
            JOIN NON_PEMAIN np ON np.id = w.id_wasit
            WHERE CONCAT(np.nama_depan, ' ', np.nama_belakang) = %s
            """, (referee_name,))
            referee_row = cur.fetchone()
            if referee_row is None:
                # Handle the case when the referee is not found
                raise Exception(f"Referee '{referee_name}' not found")
            referee_id = referee_row['id_wasit']
            referee_ids.append((referee_id, referee_position))

        stadium_name = request.session["stadium_name"]

        # Retrieve stadium ID
        cur.execute("""
        SELECT id_stadium
        FROM STADIUM
        WHERE nama = %s;
        """, (stadium_name,))
        stadium_id = cur.fetchone()['id_stadium']

        # Update PERTANDINGAN table
        cur.execute("""
        UPDATE PERTANDINGAN
        SET start_datetime = %s, end_datetime = %s, stadium = %s
        WHERE id_pertandingan = %s
        """, (start_datetime, end_datetime, stadium_id, id_pertandingan))

        # Update WASIT_BERTUGAS table
        cur.execute("""
        DELETE FROM WASIT_BERTUGAS
        WHERE id_pertandingan = %s
        """, (id_pertandingan,))
        for referee_id, referee_position in referee_ids:
            cur.execute("""
            INSERT INTO WASIT_BERTUGAS (id_wasit, id_pertandingan, posisi_wasit)
            VALUES (%s, %s, %s)
            """, (referee_id, id_pertandingan, referee_position))

        # Update TIM_PERTANDINGAN table
        cur.execute("""
        DELETE FROM TIM_PERTANDINGAN
        WHERE id_pertandingan = %s
        """, (id_pertandingan,))
        cur.execute("""
        INSERT INTO TIM_PERTANDINGAN (nama_tim, id_pertandingan, skor)
        VALUES (%s, %s, %s), (%s, %s, %s)
        """, (tim1, id_pertandingan, '0', tim2, id_pertandingan, '0'))

        # Commit the changes
        conn.commit()

        # Close the cursor
        cur.close()

        return redirect('membuat_pertandingan:show_list_pertandingan')

def update_create_match(request):
    # if request.method == "POST":
        # Process the form data
    print("test")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_panitia = get_id_panitia_loggedIn(request)


    date_value = request.session["date_value"]
    print(request.session["date_value"])


    stadium_name = request.session["stadium_name"]
    print(request.session["stadium_name"])

    print(stadium_name)


    cur.execute("""
    SELECT w.id_wasit, np.nama_depan, np.nama_belakang
    FROM WASIT w
    LEFT JOIN NON_PEMAIN np ON w.id_wasit = np.id
    WHERE w.id_wasit NOT IN (
        SELECT wb.id_wasit
        FROM WASIT_BERTUGAS wb
        INNER JOIN PERTANDINGAN p ON wb.id_pertandingan = p.id_pertandingan
        WHERE DATE(p.start_datetime) = %s
    )
    GROUP BY w.id_wasit, np.nama_depan, np.nama_belakang;
    """, (date_value,))

    wasit_list = [row['nama_depan'] + ' ' + row['nama_belakang'] for row in cur.fetchall()]  # Store the referee names in a list


    cur.execute("""
    SELECT T.nama_tim
    FROM TIM AS T
    WHERE T.nama_tim NOT IN (
        SELECT TP.nama_tim
        FROM TIM_PERTANDINGAN AS TP
        INNER JOIN PERTANDINGAN AS P ON TP.id_pertandingan = P.id_pertandingan
        WHERE DATE(%s) BETWEEN P.start_datetime::date AND P.end_datetime::date
    );
    """, (date_value,))

    team_list = [row['nama_tim'] for row in cur.fetchall()]  # Store the team names in a list

    context = {
        "id_panitia": id_panitia,
        "wasit_list": wasit_list,  # Include the referee names in the context as a list
        "team_list": team_list,  # Include the team names in the context as a list
        "date": date_value,
        "date_value": date_value,  # Add the date_value to the context
        "stadium_name":stadium_name
    }

    return render(request, "membuat_pertandingan.html", context)


def update_choose_stadium(request, id_pertandingan):
    if request.method == "POST":
        # Process the form data
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        id_panitia = get_id_panitia_loggedIn(request)

        # date_value = request.POST.get('date')
        date_value = request.session["date_value"]
        print(request.session["date_value"])


        stadium_name = request.POST.get('stadium_name')
        request.session["stadium_name"] = stadium_name
        print(request.session["stadium_name"])
        

        context = {
            "id_panitia": id_panitia,
            # "stadium_list": stadium_list,
            "date": date_value,
            "stadium_name": "",
            "date_value": date_value,
            "id_pertandingan": id_pertandingan,  # Include an empty stadium_name in the context
        }

        return render(request, "update_memilih_stadium.html", context)
    else:
        # Render the initial form
        context = {
            "stadium_name": "",  # Include an empty stadium_name in the context
        }
        return render(request, "update_memilih_stadium.html", context)
    

def update_choose_date(request, id_pertandingan):
    if request.method == "POST":
        # Process the form data
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        id_panitia = get_id_panitia_loggedIn(request)

        date_value = request.POST.get('date')
        request.session["date_value"] = date_value
        print(request.session["date_value"])
        

        cur.execute("""
        SELECT S.nama
        FROM STADIUM AS S
        WHERE S.id_stadium NOT IN (
            SELECT P.stadium
            FROM PERTANDINGAN AS P
            WHERE %s BETWEEN P.start_datetime AND P.end_datetime
        );
        """, (date_value,))

        stadium_list = [row['nama'] for row in cur.fetchall()]  # Store the stadium names in a list

        context = {
            "id_panitia": id_panitia,
            "stadium_list": stadium_list,
            "date": date_value,
            "stadium_name": "",
            "date_value": date_value,
                # Include an empty stadium_name in the context
            "id_pertandingan": id_pertandingan,
        }

        return render(request, "update_memilih_stadium.html", context)
    else:
        # Render the initial form
        context = {
            "stadium_name": "",  # Include an empty stadium_name in the context
        }
        return render(request, "update_memilih_stadium.html", context)


def choose_stadium(request):
    if request.method == "POST":
        # Process the form data
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        id_panitia = get_id_panitia_loggedIn(request)

        # date_value = request.POST.get('date')
        date_value = request.session["date_value"]
        print(request.session["date_value"])


        stadium_name = request.POST.get('stadium_name')
        request.session["stadium_name"] = stadium_name
        print(request.session["stadium_name"])
        

        # cur.execute("""
        # SELECT S.nama
        # FROM STADIUM AS S
        # WHERE S.id_stadium NOT IN (
        #     SELECT P.stadium
        #     FROM PERTANDINGAN AS P
        #     WHERE %s BETWEEN P.start_datetime AND P.end_datetime
        # );
        # """, (date_value,))

        # stadium_list = [row['nama'] for row in cur.fetchall()]  # Store the stadium names in a list

        context = {
            "id_panitia": id_panitia,
            # "stadium_list": stadium_list,
            "date": date_value,
            "stadium_name": "",
            "date_value": date_value,  # Include an empty stadium_name in the context
        }

        return render(request, "memilih_stadium.html", context)
    else:
        # Render the initial form
        context = {
            "stadium_name": "",  # Include an empty stadium_name in the context
        }
        return render(request, "memilih_stadium.html", context)
    

def choose_date(request):
    if request.method == "POST":
        # Process the form data
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        id_panitia = get_id_panitia_loggedIn(request)

        date_value = request.POST.get('date')
        request.session["date_value"] = date_value
        print(request.session["date_value"])
        

        cur.execute("""
        SELECT S.nama
        FROM STADIUM AS S
        WHERE S.id_stadium NOT IN (
            SELECT P.stadium
            FROM PERTANDINGAN AS P
            WHERE %s BETWEEN P.start_datetime AND P.end_datetime
        );
        """, (date_value,))

        stadium_list = [row['nama'] for row in cur.fetchall()]  # Store the stadium names in a list

        context = {
            "id_panitia": id_panitia,
            "stadium_list": stadium_list,
            "date": date_value,
            "stadium_name": "",
            "date_value": date_value,  # Include an empty stadium_name in the context
        }

        return render(request, "memilih_stadium.html", context)
    else:
        # Render the initial form
        context = {
            "stadium_name": "",  # Include an empty stadium_name in the context
        }
        return render(request, "memilih_stadium.html", context)







# def choose_stadium(request):
#     if request.method == "POST":
#         # Process the form data
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         id_panitia = get_id_panitia_loggedIn(request)

#         # date_value = request.POST.get('date')
#         date_value = request.session["date_value"]
#         print(request.session["date_value"])


#         stadium_name = request.POST.get('stadium_name')
#         request.session["stadium_name"] = stadium_name
#         print(request.session["stadium_name"])
        

#         # cur.execute("""
#         # SELECT S.nama
#         # FROM STADIUM AS S
#         # WHERE S.id_stadium NOT IN (
#         #     SELECT P.stadium
#         #     FROM PERTANDINGAN AS P
#         #     WHERE %s BETWEEN P.start_datetime AND P.end_datetime
#         # );
#         # """, (date_value,))

#         # stadium_list = [row['nama'] for row in cur.fetchall()]  # Store the stadium names in a list

#         context = {
#             "id_panitia": id_panitia,
#             # "stadium_list": stadium_list,
#             "date": date_value,
#             "stadium_name": "",
#             "date_value": date_value,  # Include an empty stadium_name in the context
#         }

#         return render(request, "memilih_stadium.html", context)
#     else:
#         # Render the initial form
#         context = {
#             "stadium_name": "",  # Include an empty stadium_name in the context
#         }
#         return render(request, "memilih_stadium.html", context)
    

# def choose_date(request):
#     if request.method == "POST":
#         # Process the form data
#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         id_panitia = get_id_panitia_loggedIn(request)

#         date_value = request.POST.get('date')
#         request.session["date_value"] = date_value
#         print(request.session["date_value"])
        

#         cur.execute("""
#         SELECT S.nama
#         FROM STADIUM AS S
#         WHERE S.id_stadium NOT IN (
#             SELECT P.stadium
#             FROM PERTANDINGAN AS P
#             WHERE %s BETWEEN P.start_datetime AND P.end_datetime
#         );
#         """, (date_value,))

#         stadium_list = [row['nama'] for row in cur.fetchall()]  # Store the stadium names in a list

#         context = {
#             "id_panitia": id_panitia,
#             "stadium_list": stadium_list,
#             "date": date_value,
#             "stadium_name": "",
#             "date_value": date_value,  # Include an empty stadium_name in the context
#         }

#         return render(request, "memilih_stadium.html", context)
#     else:
#         # Render the initial form
#         context = {
#             "stadium_name": "",  # Include an empty stadium_name in the context
#         }
#         return render(request, "memilih_stadium.html", context)

