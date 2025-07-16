from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from werkzeug.utils import secure_filename
from flask import current_app 
import os

auth = Blueprint("auth", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@auth.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
      session["user_id"] = user.id
      return redirect(url_for('views.home'))
    else:
      return render_template("login.html", error="Invalid username or password")
  return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)
    cover_image = request.files.get("cover_image")

    if cover_image and allowed_file(cover_image.filename):
      filename = secure_filename(cover_image.filename)
      cover_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
      cover_image_url = filename
      new_user = User(username=username, email=email, password=hashed_password, cover_image_url=cover_image_url)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for("auth.login"))
    return redirect(url_for("auth.register"))
  
  return render_template("register.html")

@auth.route("/logout")
def logout():
  session.pop("user_id", None)
  return redirect(url_for("auth.login"))
