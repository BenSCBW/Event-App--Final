from flask import render_template,request,Blueprint
from eventapp.models import EventPost
from eventapp.models import contactmodel
from eventapp.event_posts.forms import contactnow
from eventapp import db

core = Blueprint('core',__name__)

@core.route('/')
def index():
    #### Prikaz početne stranice, koristi ograničenje od 10 postova
    page = request.args.get('page', 1, type=int)
    event_posts = EventPost.query.order_by(EventPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',event_posts=event_posts)

@core.route('/info')
def info():
    #Koristi bilo koji core page, poput contact/about/page

    return render_template('info.html')

@core.route('/feedback',methods=['GET','POST'])
def contact():
    form = contactnow()

    if form.is_submitted():
        contact = contactmodel (text=form.text.data)
        db.session.add(contact)
        db.session.commit()
    return render_template('contact.html',form=form)
