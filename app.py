from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# Initialize Flask and MySQL
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_DATABASE_PASSWORD'] = 'Milind@#2429'  # Replace with your MySQL password
app.config['MYSQL_DATABASE_DB'] = 'portfolio_website'

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User loader
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    return user

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password using pbkdf2:sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Use mysql.connection to get the cursor and execute the query
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()

        flash("Registration successful", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        if user and check_password_hash(user[2], password):  # user[2] is password field
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your credentials and try again.', 'danger')

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        cur = mysql.get_db().cursor()
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", 
                    (name, email, current_user[0]))  # current_user[0] is user_id
        mysql.get_db().commit()
        flash('Profile updated successfully!', 'success')
    
    return render_template('dashboard.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
