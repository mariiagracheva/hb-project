# from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from model import connect_to_db, db, Place, Location, Opportunity, Category, PlaceCategory, OpportunityCategory, PlaceLocation, OpportunityLocation


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
# app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    return render_template("homepage.html")

@app.route('/my-location')
def my_location():
    return render_template("my_location.html")



@app.route("/places")
def places_list():
    """Show all places"""

    places = Place.query.order_by(Place.vm_id).all()
    return render_template("place_list.html", places=places)

@app.route("/opportunities")
def opps_list():
    """Show all opportunities"""

    opps = Opportunity.query.order_by(Opportunity.vm_id).all()
    print len(opps)
    return render_template("opps_list.html", opps=opps)

@app.route("/places/<vm_id>")
def show_place(vm_id):
    """Return page showing the details of organization."""

    place = Place.query.get(vm_id)
    place_location = PlaceLocation.query.filter_by(place_id=vm_id).one()
    location = Location.query.filter_by(location_id=place_location.location_id).one()

    return render_template("place_details.html",
                           place=place,
                           location=location)



@app.route("/opportunities/<vm_id>")
def show_opp(vm_id):
    """Return page showing the details of movies."""

    opp = Opportunity.query.get(vm_id)
    opp_location = OpportunityLocation.query.filter_by(opportunity_id=vm_id).one()
    location = Location.query.filter_by(location_id=opp_location.location_id).one()

    return render_template("opportunity_details.html",
                           opp=opp,
                           location=location)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')