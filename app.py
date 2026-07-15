from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret Key

app.secret_key = "mindcare_secret_key"


# MySQL Configuration

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'indhu11'

app.config['MYSQL_DB'] = 'mindcare_ai'

mysql = MySQL(app)



# ---------------- HOME ----------------

@app.route('/')

def index():

    return render_template("index.html")



# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET','POST'])

def register():

    if request.method == 'POST':

        name = request.form['name']

        email = request.form['email']

        department = request.form['department']

        year = request.form['year']

        phone = request.form['phone']

        password = request.form['password']


        hashed_password = generate_password_hash(password)


        cur = mysql.connection.cursor()


        cur.execute(

        """

        INSERT INTO student

        (name,email,department,year,phone,password)

        VALUES(%s,%s,%s,%s,%s,%s)

        """,

        (

        name,

        email,

        department,

        year,

        phone,

        hashed_password

        )

        )


        mysql.connection.commit()

        cur.close()


        flash("Registration Successful!")

        return redirect(url_for('login'))


    return render_template("register.html")



# ---------------- LOGIN ----------------
# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            SELECT student_id, name, email, password
            FROM student
            WHERE email=%s
            """,
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            stored_password = user[3]

            if check_password_hash(stored_password, password):

                session['user_id'] = user[0]
                session['username'] = user[1]

                flash("Login Successful")

                return redirect(url_for('dashboard'))

        flash("Invalid Email or Password")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')

def dashboard():

    if 'user_id' not in session:

        return redirect(url_for('login'))

    return render_template("dashboard.html")



# ---------------- ASSESSMENT ----------------
# ---------------- ASSESSMENT ----------------

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        stress_score = float(request.form['q1'])
        anxiety_score = float(request.form['q2'])
        depression_score = float(request.form['q3'])

        total_score = (
            stress_score +
            anxiety_score +
            depression_score
        )


        if total_score <= 5:
            risk_level = "Low Risk"

        elif total_score <= 10:
            risk_level = "Moderate Risk"

        else:
            risk_level = "High Risk"


        student_id = session['user_id']


        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO assessment
            (
                student_id,
                stress_score,
                anxiety_score,
                depression_score,
                risk_level
            )
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                student_id,
                stress_score,
                anxiety_score,
                depression_score,
                risk_level
            )
        )


        mysql.connection.commit()

        cur.close()


        flash(
            f"Assessment Completed! Result: {risk_level}"
        )

        return redirect(url_for('dashboard'))


    return render_template("assessment.html")


# ---------------- MOOD TRACKER ----------------
# ---------------- MOOD TRACKER ----------------

@app.route('/mood_tracker', methods=['GET', 'POST'])
def mood_tracker():

    if 'user_id' not in session:
        return redirect(url_for('login'))


    if request.method == 'POST':

        mood = request.form['mood']
        note = request.form['note']

        student_id = session['user_id']


        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO mood_tracker
            (
                student_id,
                mood,
                note,
                mood_date
            )
            VALUES (%s,%s,%s,CURDATE())
            """,
            (
                student_id,
                mood,
                note
            )
        )


        mysql.connection.commit()

        cur.close()


        flash("Mood saved successfully!")

        return redirect(url_for('mood_tracker'))


    # Show previous moods

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT mood, note, mood_date
        FROM mood_tracker
        WHERE student_id=%s
        ORDER BY mood_date DESC
        """,
        (session['user_id'],)
    )


    moods = cur.fetchall()

    cur.close()


    return render_template(
        "mood_tracker.html",
        moods=moods
    )


# ---------------- EMOTION DETECTION ----------------

# ---------------- EMOTION DETECTION ----------------

@app.route('/emotion_detection', methods=['GET','POST'])
def emotion_detection():

    if 'user_id' not in session:
        return redirect(url_for('login'))


    if request.method == 'POST':

        input_text = request.form['text']


        # Temporary emotion prediction
        # Later we will connect ML model here

        text = input_text.lower()

        if "happy" in text or "good" in text:
            emotion = "Happy"
            confidence = 0.90

        elif "sad" in text or "bad" in text:
            emotion = "Sad"
            confidence = 0.85

        elif "stress" in text or "tired" in text:
            emotion = "Stressed"
            confidence = 0.88

        else:
            emotion = "Neutral"
            confidence = 0.70



        student_id = session['user_id']


        cur = mysql.connection.cursor()


        cur.execute(
            """
            INSERT INTO emotion_detection
            (
                student_id,
                input_text,
                detected_emotion,
                confidence_score
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                student_id,
                input_text,
                emotion,
                confidence
            )
        )


        mysql.connection.commit()

        cur.close()


        flash(
            f"Emotion Detected: {emotion}"
        )


        return redirect(
            url_for('emotion_detection')
        )


    return render_template(
        "emotion_detection.html"
    )



# ---------------- CHATBOT ----------------

# ---------------- CHATBOT ----------------

@app.route('/chatbot', methods=['GET','POST'])
def chatbot():

    if 'user_id' not in session:
        return redirect(url_for('login'))


    response = ""


    if request.method == 'POST':

        message = request.form['message']


        # Temporary chatbot response
        msg = message.lower()

        if "stress" in msg:
            response = "Try deep breathing and take a short break."

        elif "sad" in msg:
            response = "I understand. Talking to someone you trust can help."

        elif "hello" in msg:
            response = "Hello! How are you feeling today?"

        else:
            response = "Thank you for sharing. I am here to support you."


        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO chatbot
            (
                student_id,
                user_message,
                bot_response
            )
            VALUES (%s,%s,%s)
            """,
            (
                session['user_id'],
                message,
                response
            )
        )

        mysql.connection.commit()

        cur.close()


    return render_template(
        "chatbot.html",
        response=response
    )



# ---------------- COUNSELING ----------------

@app.route('/counseling', methods=['GET','POST'])
def counseling():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        counselor_id = request.form['counselor_id']
        date = request.form['date']
        time = request.form['time']
        notes = request.form['notes']


        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO counseling
            (
                student_id,
                counselor_id,
                appointment_date,
                appointment_time,
                status,
                notes
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                session['user_id'],
                counselor_id,
                date,
                time,
                "Pending",
                notes
            )
        )

        mysql.connection.commit()
        cur.close()



# ---------------- PROFILE ----------------
# ---------------- PROFILE ----------------

@app.route('/profile')
def profile():

    if 'user_id' not in session:
        return redirect(url_for('login'))


    cur = mysql.connection.cursor()


    cur.execute(
        """
        SELECT 
        student_id,
        name,
        email,
        department,
        year,
        phone,
        profile_image
        FROM student
        WHERE student_id=%s
        """,
        (session['user_id'],)
    )


    student = cur.fetchone()

    cur.close()


    return render_template(
        "profile.html",
        student=student
    )





# ---------------- ADMIN ----------------
# ---------------- ADMIN ----------------

@app.route('/admin_dashboard')
def admin_dashboard():

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM student")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assessment")
    total_assessments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM mood_tracker")
    total_moods = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM emotion_detection")
    total_emotions = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM counseling")
    total_counseling = cur.fetchone()[0]

    cur.close()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_assessments=total_assessments,
        total_moods=total_moods,
        total_emotions=total_emotions,
        total_counseling=total_counseling
    )
# ---------------- LOGOUT ----------------

@app.route('/logout')

def logout():

    session.clear()

    flash("Logged Out Successfully")

    return redirect(url_for('login'))



# ---------------- RUN ----------------

if __name__ == "__main__":

    app.run(

    debug=True

    )