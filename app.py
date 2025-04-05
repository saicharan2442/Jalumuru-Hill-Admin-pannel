from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2442",
    database="jalumuru_hill"
)
cursor = conn.cursor()

# ---------- INDEX PAGE ----------
@app.route('/')
def index():
    return render_template('index.html')

# ---------- TEMPLE ROUTES ----------
@app.route('/temples', methods=['GET', 'POST'])
def temples():
    if request.method == 'POST':
        image_url = request.form['image_url']
        tname = request.form['tname']
        donar = request.form['donar']
        village = request.form['village']
        district = request.form['district']
        ph_no = request.form['ph_no']

        query = """
            INSERT INTO temples (image_url, tname, donar, village, district, ph_no)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (image_url, tname, donar, village, district, ph_no)
        cursor.execute(query, values)
        conn.commit()
        return redirect(url_for('temples'))

    cursor.execute("SELECT id, image_url, tname, donar, village, district, ph_no FROM temples ORDER BY id DESC")
    temples = cursor.fetchall()
    return render_template('temples.html', temples=temples)

@app.route('/delete_temple/<int:id>')
def delete_temple(id):
    cursor.execute("DELETE FROM temples WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('temples'))

@app.route('/edit_temple/<int:id>', methods=['GET', 'POST'])
def edit_temple(id):
    if request.method == 'POST':
        image_url = request.form['image_url']
        donar = request.form['donar']
        village = request.form['village']
        district = request.form['district']
        ph_no = request.form['ph_no']

        query = """
            UPDATE temples SET image_url=%s, donar=%s, village=%s,
            district=%s, ph_no=%s WHERE id=%s
        """
        values = (image_url, donar, village, district, ph_no, id)
        cursor.execute(query, values)
        conn.commit()
        return redirect(url_for('temples'))

    cursor.execute("SELECT * FROM temples WHERE id = %s", (id,))
    temple = cursor.fetchone()
    return render_template('edit_temple.html', temple=temple)

# ---------- DONAR ROUTES ----------
@app.route('/donars', methods=['GET', 'POST'])
def donars():
    if request.method == 'POST':
        name = request.form['name']
        village = request.form['village']
        district = request.form['district']
        email = request.form['email']
        phone_number = request.form['phone_number']
        donated = request.form['donated']

        cursor.execute("""
            INSERT INTO donars (Name, village, district, email, phone_number, donated)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, village, district, email, phone_number, donated))
        conn.commit()
        return redirect(url_for('donars'))

    cursor.execute("SELECT * FROM donars ORDER BY id DESC")
    donars = cursor.fetchall()
    return render_template('donars.html', donars=donars)

@app.route('/edit_donar/<int:id>', methods=['GET', 'POST'])
def edit_donar(id):
    if request.method == 'POST':
        name = request.form['name']
        village = request.form['village']
        district = request.form['district']
        email = request.form['email']
        phone_number = request.form['phone_number']
        donated = request.form['donated']

        cursor.execute("""
            UPDATE donars SET Name=%s, village=%s, district=%s, email=%s, phone_number=%s, donated=%s WHERE id=%s
        """, (name, village, district, email, phone_number, donated, id))
        conn.commit()
        return redirect(url_for('donars'))

    cursor.execute("SELECT * FROM donars WHERE id = %s", (id,))
    donar = cursor.fetchone()
    return render_template('edit_donar.html', donar=donar)

@app.route('/delete_donar/<int:id>')
def delete_donar(id):
    cursor.execute("DELETE FROM donars WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('donars'))

# ---------- EVENTS ROUTES ----------
@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        image_url = request.form['image_url']
        eventname = request.form['eventname']
        event_date = request.form['event_date']
        event_temple = request.form['event_temple']
        discription = request.form['discription']

        cursor.execute("""
            INSERT INTO events (eventname, event_date, event_temple, discription, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (eventname, event_date, event_temple, discription, image_url))
        conn.commit()
        return redirect(url_for('events'))

    cursor.execute("SELECT * FROM events ORDER BY id DESC")
    events = cursor.fetchall()
    return render_template('events.html', events=events)

@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    if request.method == 'POST':
       
        eventname = request.form['eventname']
        event_date = request.form['event_date']
        event_temple = request.form['event_temple']
        discription = request.form['discription']

        cursor.execute("""
            UPDATE events SET eventname=%s, event_date=%s, event_temple=%s, discription=%s WHERE id=%s
        """, (eventname, event_date, event_temple, discription, id))
        conn.commit()
        return redirect(url_for('events'))

    cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = cursor.fetchone()
    return render_template('edit_event.html', event=event)

@app.route('/delete_event/<int:id>')
def delete_event(id):
    cursor.execute("DELETE FROM events WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('events'))

# ---------- EBOOK ROUTES ----------
@app.route('/ebooks', methods=['GET', 'POST'])
def ebooks():
    if request.method == 'POST':
        name = request.form['name']
        format = request.form['format']
        size = request.form['size']
        download_link = request.form['download_link']
        image_url = request.form.get('image_url')  # get() to avoid KeyError if missing

        cursor.execute("""
            INSERT INTO ebooks (name, format, size, download_link, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, format, size, download_link, image_url))
        conn.commit()
        return redirect(url_for('ebooks'))

    cursor.execute("SELECT * FROM ebooks")
    ebooks = cursor.fetchall()
    return render_template('ebook.html', ebooks=ebooks)


@app.route('/edit_ebook/<int:id>', methods=['GET', 'POST'])
def edit_ebook(id):
    if request.method == 'POST':
        name = request.form['name']
        format = request.form['format']
        size = request.form['size']
        download_link = request.form['download_link']
        image_url = request.form.get('image_url')  # Safe fetch

        cursor.execute("""
            UPDATE ebooks
            SET name=%s, format=%s, size=%s, download_link=%s, image_url=%s
            WHERE id=%s
        """, (name, format, size, download_link, image_url, id))
        conn.commit()
        return redirect(url_for('ebooks'))

    cursor.execute("SELECT * FROM ebooks WHERE id = %s", (id,))
    ebook = cursor.fetchone()
    return render_template('edit_ebook.html', ebook=ebook)


@app.route('/delete_ebook/<int:id>')
def delete_ebook(id):
    cursor.execute("DELETE FROM ebooks WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('ebooks'))


# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True)
