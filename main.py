from flask import Flask,render_template,request,url_for,redirect
import sqlite3
from adminpanel import Admin_panel

app = Flask(__name__)
adm_make_table = Admin_panel('Alex', 'qwerty123456')

@app.route('/adminpanel_make_time')
def adm_make_time():
    return render_template('adm_panel.html')


@app.route('/places', methods=['GET','POST'])
def places():
    conn = sqlite3.connect('ticketbase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT place,is_free_place FROM work_time_ GROUP BY place LIMIT 251')
    place_result = cursor.fetchall()
    cursor.execute('SELECT is_free_place FROM work_time_')

    places = [(row[0], row[1]) for row in place_result]
    selected_places = request.form.getlist('place')

    day = request.args.get('day')
    time = request.args.get('time')
    print(day)
    print(time)

    conn.commit()
    conn.close()
    return render_template('places.html',places = places[1:], day=day, time=time )

@app.route('/pay_page', methods=['GET','POST'])
def pay_page_panel():
    conn = sqlite3.connect('ticketbase.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        selected_places = request.form.getlist('place')
        day = request.form['day']
        time = request.form['time']
        print(day)
        print(time)
        print(selected_places)
        for i in selected_places:
            cursor.execute("UPDATE work_time_ SET is_free_place = 0 WHERE id = ? AND time = ? AND place = ?",(day, time, i))
            print(i)
        conn.commit()
        conn.close()
        return render_template('pay_page.html', selected_places=selected_places, day=day, time=time)
    else:
        return redirect(url_for('places'))




@app.route('/', methods=['GET', 'POST'])
def user_panel():
    conn = sqlite3.connect('ticketbase.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        day = request.form['day']
        time = request.form['time'].split(',')
        adm_make_table.make_table(str(day),time)

        print(' Значения добавлены!')

    #cursor.execute('SELECT DISTINCT id, time, GROUP_CONCAT(time) FROM work_time_ GROUP BY time')
    cursor.execute('SELECT DISTINCT id, time FROM work_time_')

    day_id = cursor.fetchall()
    day_time = {}

    conn.commit()
    conn.close()
    days = set([day for day, *_ in day_id])
    times = set([time for time,*_ in day_id ])

    for day, time,*_ in day_id:
        if day not in day_time:
            day_time[day] = []
        day_time[day].append(time)

    for day, time_list in day_time.items():
        print(f"День: {day}")
        print("Время:")
        for time in time_list:
            print(time)
        print("---")

    return render_template('index.html', day_time=day_time, days=days)

if __name__ =='__main__':
    app.run()