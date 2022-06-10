from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.post import Post

@app.route('/post_message',methods=['POST'])
def post_message():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "user_id": session["user_id"],
        "community_id": request.form['community_id'],
        "content": request.form['content']

    }
    Post.save(data)
    return redirect(f'/view/{request.form["id"]}')
