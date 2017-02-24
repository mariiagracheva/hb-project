# from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from model import connect_to_db, db, Place, Location, Opportunity, Category, PlaceCategory, OpportunityCategory


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
# app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage. Map with current user location"""
    return render_template("homepage.html")

# @app.route('/my-location')
# def my_location():
#     return render_template("my_location.html")


@app.route("/places")
def places_list():
    """Show all places"""

    places = Place.query.order_by(Place.name).all()
    print places
    return render_template("place_list.html", places=places)

@app.route("/places/<vm_id>")
def show_place(vm_id):
    """Return page showing the details of places."""

    print vm_id
    place = Place.query.get(vm_id)
    print place
    print place.vm_id
    print place.name

    return render_template("place_details.html",
                           display_place=place)

@app.route("/opportunities")
def opps_list():
    """Show all opportunities"""

    opps = Opportunity.query.order_by(Opportunity.title).all()
    print opps
    return render_template("opps_list.html", opps=opps)



@app.route("/opportunities/<vm_id>")
def show_opp(vm_id):
    """Return page showing the details of opportunities."""

    print vm_id
    opp = Opportunity.query.get(vm_id)
    print opp
    print opp.vm_id
    print opp.title
    return render_template("opportunity_details.html",
                           display_opp=opp)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')