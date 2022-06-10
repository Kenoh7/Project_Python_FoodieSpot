from flask import render_template,redirect,session,request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.food import Food

@app.route('/food')
def food_search():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('food.html',user=User.get_by_id(data), foods=Food.foods_to_user())

@app.route('/food/results')
def food_results():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('results.html',user=User.get_by_id(data))

@app.route('/food/view')
def food_view():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('view.html',user=User.get_by_id(data))

@app.route('/add',methods=['POST'])
def add_food():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session["user_id"],
        "ingredient": request.form["ingredient"],
    }
    Food.save(data)
    return redirect('/food')