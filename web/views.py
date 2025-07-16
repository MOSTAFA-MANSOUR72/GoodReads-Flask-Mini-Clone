from flask import Blueprint, render_template, request
from flask import session, redirect, url_for
from .models import book, User, activity, currently_reading, completed_books
from . import db
from werkzeug.utils import secure_filename
from flask import current_app 
import os


views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def home():
    if session.get("user_id"):
        user_id = session["user_id"]
        books = User.query.filter_by(id=user_id).first().currently_reading_books
        current_reading_books = {
            entry.book_id: entry.page_number for entry in db.session.query(currently_reading).filter_by(user_id=user_id).all()
            }
        local_completed_books = {
            entry.book_id: entry.completion_date for entry in db.session.query(completed_books).filter_by(user_id=user_id).all()
            }
        followed_users_ids = [user.id for user in 
                              db.session.query(User).filter(User.id != user_id).all()
                                if user in db.session.query(User).filter_by(id=user_id).first().followers
            ]
        posts = db.session.query(activity).filter(activity.user_id.in_(followed_users_ids)).all()
        followed_users = db.session.query(User).filter_by(id=user_id).first().followers
        return render_template(
            "current_reading_books.html",
            books=books,
            title="Currently Reading",
            current_reading_books=current_reading_books,
            local_completed_books=local_completed_books,
            activities=posts,
            followed_users=followed_users
            )
    else:
        return redirect(url_for('auth.login'))
    
@views.route('/MyBooks', methods=["GET", "POST"])
def MyBooks():
    if session.get("user_id"):
        user_id = session["user_id"]
        books = book.query.filter_by(user_id=user_id).all()
        current_reading_books = [
            entry.book_id for entry in db.session.query(currently_reading).filter_by(user_id=user_id).all()
            ]
        local_completed_books = {
            entry.book_id: entry.completion_date for entry in db.session.query(completed_books).filter_by(user_id=user_id).all()
            }
        
        return render_template(
            "container.html",
            books=books,
            title="My Books",
            current_reading_books=current_reading_books,
            local_completed_books=local_completed_books,
            user_id=user_id
            )
    else:
        return redirect(url_for('auth.login'))
    
@views.route('/Explore', methods=["GET"])
def explore():
    if session.get("user_id"):
        user_id = session["user_id"]
        books = book.query.all()
        current_reading_books = [
            entry.book_id for entry in db.session.query(currently_reading).filter_by(user_id=user_id).all()
            ]
        local_completed_books = {
            entry.book_id: entry.completion_date for entry in db.session.query(completed_books).filter_by(user_id=user_id).all()
            }
        users = db.session.query(User).filter(User.id != user_id).all()
        followed_users = db.session.query(User).filter_by(id=user_id).first().followers
        return render_template(
            "explore.html", 
            books=books, 
            title="Explore", 
            current_reading_books=current_reading_books,
            local_completed_books=local_completed_books,
            users = users,
            followed_users=followed_users
            )
    else:
        return redirect(url_for('auth.login'))
    
@views.route('/completedBooks', methods=["GET"])
def completedBooks():
    if session.get("user_id"):
        user_id = session["user_id"]
        books = User.query.filter_by(id=session["user_id"]).first().completed_books
        local_completed_books = {
            entry.book_id: entry.completion_date for entry in db.session.query(completed_books).filter_by(user_id=user_id).all()
            }
        return render_template(
            "container.html", 
            books=books, 
            title="Completed Books",
            local_completed_books=local_completed_books
            )
    else:
        return redirect(url_for('auth.login'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/addBook', methods=["GET", "POST"])
def addBook():
    if session.get("user_id"):
        user_id = session["user_id"]
        if request.method == "POST":
            title = request.form.get("title")
            author = request.form.get("author")
            description = request.form.get("description")
            cover_image = request.files.get("cover_image")
            pages_number = request.form.get("pages_number")
            if cover_image and allowed_file(cover_image.filename):
              filename = secure_filename(cover_image.filename)
              cover_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
              cover_image_url = filename
              new_book = book(
                  user_id=user_id,
                  title=title,
                  author=author,
                  description=description,
                  cover_image_url=cover_image_url,
                  pages_number=pages_number
              )
              new_activity = activity(
                  user_id = user_id,
                  action=f"added a new book: {title}",
                  user= db.session.query(User).filter_by(id=user_id).first()
              )
              db.session.add(new_activity)
              db.session.add(new_book)
              db.session.commit()
              return redirect(url_for('views.MyBooks'))
        return render_template("add-book.html")

    else:
        return redirect(url_for('auth.login'))
    
@views.route('/update_currently_reading/<int:book_id>', methods=["POST"])
def update_currently_reading(book_id):
    if session.get("user_id"):
        user_id = session["user_id"]

        book_to_update = db.session.query(currently_reading).filter_by(book_id=book_id, user_id=user_id).first()
        if book_to_update:
            db.session.query(currently_reading).filter_by(book_id=book_id, user_id=user_id).delete()
            db.session.commit()
        else:
            new_activity = activity(
                user_id=user_id,
                action= f"started to read the book: {db.session.query(book).filter_by(id=book_id).first().title}",
                user= db.session.query(User).filter_by(id=user_id).first()
            )
            db.session.add(new_activity)
            db.session.execute(currently_reading.insert().values(book_id=book_id, user_id=user_id, page_number=0))
            db.session.commit()
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))
    
@views.route('/update_progress/<int:book_id>', methods=["POST"])
def update_progress(book_id):
    if session.get("user_id"):
        user_id = session["user_id"]
        page_number = request.form.get("current_page")
        total_pages = int(book.query.filter_by(id=book_id).first().pages_number)
        current_book = db.session.query(book).filter_by(id=book_id).first()
        book_to_update = db.session.query(currently_reading).filter_by(book_id=book_id, user_id=user_id).first()
        if book_to_update:
            db.session.query(currently_reading).filter_by(book_id=book_id, user_id=user_id).update({"page_number": page_number})
            db.session.commit()
            if int(page_number) == total_pages:
                db.session.execute(
                    completed_books.insert().values(
                        book_id=book_id, 
                        user_id=user_id, 
                        completion_date=db.func.now()
                        )
                    )
                new_activity = activity(
                    user_id= user_id,
                    action= f"finished reading the book: {current_book.title}",
                    user= db.session.query(User).filter_by(id=user_id).first()
                )
                db.session.add(new_activity)
                db.session.query(currently_reading).filter_by(book_id=book_id, user_id=user_id).delete()
                db.session.commit()
                return redirect(url_for('views.completedBooks'))
            new_activity = activity(
                user_id= user_id,
                action= f"have read {page_number} pages of the book: {current_book.title}",
                user= db.session.query(User).filter_by(id=user_id).first()
            )
            db.session.add(new_activity)
            db.session.commit()
        return redirect(url_for('views.home'))
    
@views.route('/delete_completed_book/<int:book_id>', methods=["POST"])
def delete_completed_book(book_id):
    if session.get("user_id"):
        user_id = session["user_id"]
        db.session.query(completed_books).filter_by(book_id=book_id, user_id=user_id).delete()
        db.session.commit()
        return redirect(url_for('views.completedBooks'))
    

@views.route('/delete_book/<int:book_id>', methods=["POST"])
def delete_book(book_id):
    if session.get("user_id"):
        user_id = session["user_id"]
        db.session.query(book).filter_by(id=book_id, user_id=user_id).delete()
        db.session.commit()
        return redirect(url_for('views.MyBooks'))
    else:
        return redirect(url_for('auth.login'))
    
@views.route('/update_book/<int:book_id>', methods=["GET","POST"])
def update_book(book_id):
    if session.get("user_id"):
        user_id = session["user_id"]
        book_to_update = book.query.filter_by(id=book_id, user_id=user_id).first()
        if not book_to_update:
            return redirect(url_for('views.MyBooks'))

        if request.method == "POST":
            title = request.form.get("title")
            author = request.form.get("author")
            description = request.form.get("description")
            pages_number = request.form.get("pages_number")
            cover_image = request.files.get("cover_image")
          
            book_to_update.title = title
            book_to_update.author = author
            book_to_update.description = description
            book_to_update.pages_number = pages_number
            if cover_image and allowed_file(cover_image.filename):
                filename = secure_filename(cover_image.filename)
                cover_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                book_to_update.cover_image_url = filename
            db.session.commit()
            return redirect(url_for('views.MyBooks'))

        return render_template("edit-book.html", book=book_to_update)
    else:
        return redirect(url_for('auth.login'))


@views.route('follow/<int:user_id>', methods=["POST"])
def follow(user_id):
    if session.get("user_id"):
        current_user_id = session["user_id"]
        current_user = User.query.filter_by(id=current_user_id).first()
        user_to_follow = User.query.filter_by(id=user_id).first()
        if current_user and user_id != current_user_id:
            current_user.follow(user_to_follow)
            db.session.commit()
            return redirect(url_for('views.explore'))
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('auth.login'))
    
@views.route('unfollow/<int:user_id>', methods=["POST"])
def unfollow(user_id):
    if session.get("user_id"):
        current_user_id = session["user_id"]
        current_user = User.query.filter_by(id=current_user_id).first()
        user_to_unfollow = User.query.filter_by(id=user_id).first()
        if current_user and user_id != current_user_id:
            current_user.unfollow(user_to_unfollow)
            db.session.commit()
        return redirect(url_for('views.explore'))
    else:
        return redirect(url_for('auth.login'))
    
@views.route('profile', methods=["GET"])
def profile():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(id=user_id).first()
        current_reading_books_number = len(user.currently_reading_books)
        completed_books_number = len(user.completed_books)
        my_books_number = len(user.books)
        return render_template(
            "profile.html", 
            user=user, 
            current_reading_books_number=current_reading_books_number,
            completed_books_number=completed_books_number,
            my_books_number=my_books_number,
            )
    else:
        return redirect(url_for('auth.login'))