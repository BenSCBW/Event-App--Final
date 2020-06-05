import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__ , static_url_path='/static')
Bootstrap(app)

app.config['SECRET_KEY'] = 'mysecret'

                                                                ####################
                                                                ### BAZA PODATAKA###
                                                                ####################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)

                                          ############################### LOGIN KONFIGURACIJA ##################################

login_manager = LoginManager()

#  predaj aplikaciji do login managera
login_manager.init_app(app)

# NA KOJI VIEW SE IDE NAKON ŠTO SE KORISNIK ULONGIRA
login_manager.login_view = "users.login"


                                                            #################################
                                                            #### BLUEPRINT KONFIGURACIJA ####
                                                            #################################

from eventapp.core.views import core
from eventapp.users.views import users
from eventapp.event_posts.views import event_posts
from eventapp.error_pages.handlers import error_pages

# registracija apps-a
app.register_blueprint(users)
app.register_blueprint(event_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)
