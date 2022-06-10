from flask import render_template, request, redirect,flash,session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.community import Community
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# display routes -----------------------------------------------------
@app.route('/')
def main():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('index.html')

@app.route('/home')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    print(data)
    return render_template("home.html",user=User.get_by_id(data), communities=Community.communities_to_user())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# active routes ---------------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    if not User.is_valid(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/home')

@app.route("/login", methods=["POST"])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("- Invalid Email/Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("- Invalid Email/Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/home')