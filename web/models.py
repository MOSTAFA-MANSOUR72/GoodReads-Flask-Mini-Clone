from . import db

currently_reading = db.Table('currently_reading',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('page_number', db.Integer, nullable=False)
)

completed_books = db.Table('completed_books',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('completion_date', db.DateTime, nullable=False)
)

followers = db.Table('followers',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    cover_image_url = db.Column(db.String(500), nullable=False)
    currently_reading_books = db.relationship(
        'book',
        secondary=currently_reading,
        back_populates='reader_users'
    )
    completed_books = db.relationship(
        'book',
        secondary=completed_books,
        back_populates='completed_by_users'
    )
    followers = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followed_by', lazy='dynamic'),
        lazy='dynamic'
    )
    books = db.relationship('book', back_populates='owner')
    def __init__(self, username, email, password, cover_image_url):
        self.username = username
        self.email = email
        self.password = password
        self.cover_image_url = cover_image_url
    
    def is_following(self, user):
        return self.followers.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followers.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followers.remove(user)

class activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='activities')
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __init(self, user_id, action):
        self.user_id = user_id
        self.action= action

class book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    cover_image_url = db.Column(db.String(500))
    pages_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    owner = db.relationship('User', back_populates='books')
    reader_users = db.relationship(
        'User',
        secondary=currently_reading,
        back_populates='currently_reading_books'
    )
    completed_by_users = db.relationship(
        'User',
        secondary=completed_books,
        back_populates='completed_books'
    )
    def __init__(self, title, author, user_id, pages_number, description, cover_image_url):
        self.title = title
        self.author = author
        self.user_id = user_id
        self.pages_number = pages_number
        self.description = description
        self.cover_image_url = cover_image_url