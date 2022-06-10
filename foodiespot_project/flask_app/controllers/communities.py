from flask import render_template,redirect,session,request
from flask_app import app
from flask_app.models.community import Community
from flask_app.models.user import User
from flask_app.models.post import Post

# display route --------------------------------------------------------------
@app.route('/create')
def add_community():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('create_post.html',user=User.get_by_id(data))

@app.route('/edit/<int:id>')
def edit_community(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_post.html",edit=Community.get_one(data),user=User.get_by_id(user_data))

@app.route('/delete/<int:id>')
def delete_community(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Community.delete(data)
    return redirect('/home')

@app.route('/view/<int:id>')
def view_community(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view_post.html",user=User.get_by_id(user_data),community=Community.onecommunity_to_user(data), posts=Post.posts_to_user())
# active route --------------------------------------------------------------

@app.route('/new',methods=['POST'])
def create_community():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Community.is_valid(request.form):
        return redirect('/create')
    data = {
        "user_id": session["user_id"],
        "title": request.form["title"],
        "description": request.form["description"]
    }
    Community.save(data)
    return redirect('/home')

@app.route('/reply',methods=['POST'])
def create_reply():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Community.post_is_valid(request.form):
        return redirect(f'/view/{request.form["id"]}')
    data = {
        "user_id": session["user_id"],
        "post": request.form["post"]
    }
    Community.save(data)
    return redirect('/home')

@app.route('/update',methods=['POST'])
def update_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Community.is_valid(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    data = {
        "user_id": session["user_id"],
        "title": request.form["title"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    Community.update(data)
    return redirect('/home')