from eventapp import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from sqlalchemy import update
from flask_bootstrap import Bootstrap
from flask_login import LoginManager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('EventPost', backref='author', lazy=True)
    comment = db.relationship('Comment', backref='author', lazy=True)

    def blog_posts(self):
        return EventPost.query.order_by(EventPost.timestamp.desc())

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"



class EventPost(db.Model):
    # Setup odnosa za tablicu user
    users = db.relationship(User)

    # Model za event Posts ona Website-u
    id = db.Column(db.Integer, primary_key=True)
    #  event post= spojen odredjenom autoru
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='title', lazy='dynamic')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)
    city= db.Column(db.String(100), nullable=False)
    address= db.Column(db.String(100), nullable=False)
    time_start = db.Column(db.String(100), nullable=False)
    time_end = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    pic = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)

    def get_comments(self):
        return Comment.query.filter_by(post_id=EventPost.id).order_by(Comment.timestamp.desc())

    def __init__(self, title, text, time_start, time_end, city, user_id, pic, contact, address):
        self.title = title
        self.text = text
        self.contact = contact
        self.city = city
        self.time_start = time_start
        self.time_end = time_end
        self.address = address
        self.user_id = user_id
        self.pic = pic


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title} --- Location: {self.city} --- Time_Start: {self.time_start} --- Time_End: {self.time_end} --- Address: {self.address} --- Contact: {self.contact}"

class Comment(db.Model):
    post = db.relationship(EventPost)
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('event_post.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class contactmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, text):
        self.text = text
