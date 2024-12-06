from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import supabase

app = Flask(__name__)
app.secret_key = "your_secret_key"
bcrypt = Bcrypt(app)

SUPABASE_URL = "https://ebdwgxrcpfipbgmjiktx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImViZHdneHJjcGZpcGJnbWppa3R4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMyMzczNzMsImV4cCI6MjA0ODgxMzM3M30.ROkctnTe9GvarxnrAkSYNBLMBzzL8lByRqE1F3ry4Xg"
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    is_logged_in = session.get('logged_in', False)
    return render_template('homepage.html', is_logged_in=is_logged_in)

@app.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("apply"))

        existing_user = supabase_client.table("users").select("*").eq("username", username).execute()

        if existing_user.data:
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for("apply"))

        supabase_client.table("users").insert({
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password, 
            "role": "user"
        }).execute()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("apply.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check the user's credentials
        response = supabase_client.table("users").select("*").eq("username", username).execute()
        
        if not response.data:
            flash("User not found!", "error")
            return redirect(url_for("login"))
        
        user = response.data[0]
        
        # Check if the password matches
        if user["password"] != password:
            flash("Incorrect password. Please try again.", "error")
            return redirect(url_for("login"))
        
        # Store user data in session
        session['logged_in'] = True
        session['user_id'] = user['id']
        session['role'] = user['role']  # Store the role in the session

        # Debugging: print the session data
        print(f"Session after login: {session}")

        # Redirect based on user role
        if user["role"] == "admin":
            flash("Welcome, Admin!", "success")
            return redirect(url_for("homepage"))
        elif user["role"] == "user":
            flash("Welcome, User!", "success")
            return redirect(url_for("homepage"))
        else:
            flash("Role not recognized.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/homepage')
def homepage():
    is_logged_in = session.get('logged_in', False)
    return render_template('homepage.html', is_logged_in=is_logged_in)

@app.route('/about')
def about():
    if 'user_id' in session:
        return render_template('about.html', logged_in=True)
    else:
        return render_template('about.html', logged_in=False)

@app.route('/documents')
def documents():
    if 'user_id' in session:
        return render_template('documents.html', logged_in=True)
    else:
        return render_template('documents.html', logged_in=False)

@app.route('/fill_out')
def fill_out():
    if 'user_id' in session:
        return render_template('fill_out.html', logged_in=True)
    else:
        return render_template('fill_out.html', logged_in=False)

@app.route('/information')
def information():
    if 'user_id' in session:
        return render_template('information.html', logged_in=True)
    else:
        return render_template('information.html', logged_in=False)

@app.route('/loan_history')
def loan_history():
    if 'user_id' in session:
        return render_template('loan_history.html', logged_in=True)
    else:
        return render_template('loan_history.html', logged_in=False)

@app.route('/order')
def order():
    if 'user_id' in session:
        return render_template('order.html', logged_in=True)
    else:
        return render_template('order.html', logged_in=False)

@app.route('/personal_info')
def personal_info():
    if 'user_id' in session:
        return render_template('personal_info.html', logged_in=True)
    else:
        return render_template('personal_info.html', logged_in=False)

@app.route('/privacy_policy')
def privacy_policy():
    if 'user_id' in session:
        return render_template('privacy_policy.html', logged_in=True)
    else:
        return render_template('privacy_policy.html', logged_in=False)

@app.route('/status')
def status():
    if 'user_id' in session:
        return render_template('status.html', logged_in=True)
    else:
        return render_template('status.html', logged_in=False)

@app.route('/verification')
def verification():
    if 'user_id' in session:
        return render_template('verification.html', logged_in=True)
    else:
        return render_template('verification.html', logged_in=False)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
