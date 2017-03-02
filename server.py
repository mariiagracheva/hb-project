# from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from model import connect_to_db, db, Place, Location, Opportunity, Category, PlaceCategory, OpportunityCategory, PlaceLocation, OpportunityLocation
import json

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

@app.route("/test")
def test():

    # opps = list(Opportunity.query.all())
    # print type(opps)
    # print opps[1]
    # print type(json.dumps(opps))

    data = {}
    #print type(data)

    opportunity_location = OpportunityLocation.query.all()

    for opp_loc in opportunity_location:
        # print type(opp_loc)
        opp = opp_loc.opportunity_id
        loc = Location.query.filter_by(location_id=opp_loc.location_id).one()


        data[opp] = '%s,%s' %(loc.lat, loc.lng)
    
    #print data


    return render_template("test.html")


@app.route("/format-data")
def format_data():
    # print "\n\n"
    # print "INSIDE FORMAT_DATA ROUTE"
    data = {}
    # print type(data)

    opportunity_location = OpportunityLocation.query.all()
    # print "\n\n"
    for opp_loc in opportunity_location:
        opp = opp_loc.opportunity_id
        opp_data = Opportunity.query.filter_by(vm_id=opp).one()
        loc = Location.query.filter_by(location_id=opp_loc.location_id).one()

        # 0 - lat
        # 1 - lng
        # 2 - img_url
        # 3 - descr
        # 4 - categoryIds
        # 5 - title
        # 6 - tags
        # 7 - opp_time
        data[opp] = '%s,%s,%s,%s,%s,%s,%s,%s' %(loc.lat, loc.lng, opp_data.img_url, opp_data.descr, opp_data.categoryIds, opp_data.title, opp_data.tags, opp_data.opp_time)

    print type(data.keys())

    return jsonify(data)


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/get-results")
def return_search_results():
    data = {}
    # print "!!!!!!!!!!"
    searchquery = str(request.args.get('searchquery'))
    print searchquery
    # found_opps = Opportunity.query.limit(10).all()
    found_opps = Opportunity.query.filter(Opportunity.title.like("%"+searchquery+"%")).limit(100).all()
    for opp in found_opps:
        data[opp.vm_id] = opp.title
        # loc = OpportunityLocation.query.filter_by(opportunity_id=opp).one()
        # data[opp.vm_id].append([loc.lat, loc.lng])

        # print opp.vm_id, data[opp.vm_id]
    # print (found_opps)
    # print json.dumps(data)

    return jsonify(data)






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')