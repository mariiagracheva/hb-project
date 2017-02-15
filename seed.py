from sqlalchemy import func
from model import Place
from model import Opportunity
from model import Category
from model import Location
from model import PlaceCategory
from model import OpportunityCategory 
import datetime

from model import connect_to_db, db
from server import app
import os
import re




def load_locations():
    """Load locations from opp_json/*.json and org_json/*.json"""

    print "Locations"
    Location.query.delete()

    directories = ['opp_json', 'org_json']
    for path in directories
        listing = os.listdir(path)
        for infile in listing:
            
            # extract opportunity id
            s = infile.name
            start = s.index(start) + len(start)
            stop = s.index(end, start)
            vm_id = s[start:stop]
            
            # get location's data
            data = json.loads(open(infile).read())

            lat = data['latitude']
            lng = data['longitude']
            st_add1 = data['street-address']
            st_add2 = data['street-address2']
            city = data['city']
            zip_code = data['zip_code']

            location = Location(lat=lat,
                                lng=lng,
                                st_add1=st_add1,
                                st_add2=st_add2,
                                city=city,
                                zip_code=zip_code)
            db.session.add(location)

        db.session.commit()




def load_places():
    """Load places(rganizations) from org_json/"""
    print "Places"

    f = open('orgs.json')
    for line in f:
        for org in json.loads(line)['organizations']:
            
            vm_id = org['id'] 
            descr = org['plaintextDescription']
            img_url = org['imageUrl']
            place_type = org['type']
            name = org['name']


def load_ratings():
    """Load ratings from u.data into database."""
    print "Ratings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, place_id, score, timestamp  = row.split("\t")

        rating = Rating(place_id=place_id,
                        user_id=user_id,
                        score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

    # Once we're done, we should commit our work
    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_places()
    load_ratings()
    set_val_user_id()
