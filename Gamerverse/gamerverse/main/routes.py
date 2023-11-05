from flask import render_template, request, Blueprint
from gamerverse.models import Event

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Event.query.order_by(Event.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/calendar")
def calendar():
    events = Event.query.order_by(Event.date_posted.desc())
    return render_template('calendar.html', title='Calendar', events=events)

@main.route("/location")
def location():
    return render_template('location.html', title='Location')