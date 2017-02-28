from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from model import Place
from model import Opportunity
from model import Category
from model import Location
from model import PlaceCategory
from model import OpportunityCategory
from model import PlaceLocation
from model import OpportunityLocation

import datetime

from model import connect_to_db, db
from server import app
import os
import json


# ========= Load places and locations from htmls ============================== 
def load_places_and_locations():
    """Load places from org_html/* and update with data from organizations.json"""
    print 'load_places_and_locations()'
    
    dir = 'org_html'
    listing = os.listdir(dir)
    for infile in listing:
        # extract organization's id
        vm_id = int(infile.split('.')[0])
        data = json.loads(open(dir+'/'+infile).read())
        # get location's data
        lat = data['latitude']
        lng = data['longitude']
        try:
            st_add1 = data['street-address']
        except:
            st_add1 = ''
        try:
            st_add2 = data['street-address2']
        except:
            st_add2 = ''
        try:
            city = data['city']
        except:
            city = ''
        try:
            zip_code = data['zip_code']
        except:
            zip_code = ''
        

        location = Location(lat=lat,
                            lng=lng,
                            st_add1=st_add1,
                            st_add2=st_add2,
                            city=city,
                            zip_code=zip_code)
        place = Place(vm_id=vm_id)

        db.session.add(location)
        db.session.add(place)
        db.session.commit()

# ========= Update places with API data =======================================
def update_places():

    print 'update_places()'

    for line in open('organizations.json'):
         for org in json.loads(line)['organizations']:
            # checking if org['id'] is in places table and update
            try:
                place = Place.query.filter_by(vm_id=org['id']).one()
                place.name = org['name']
                place.place_type = org['type']
                place.img_url = org['imageUrl']
                place.descr = org['description']
                place.mission = org['mission']
                place.categoryIds = json.dumps(org['categoryIds'])

                db.session.commit()
                print "place updated"
            
            except:
                print 'Place with no opportunities'
                continue

# ========= Load opps and locations from htmls ================================         
def load_opportunities_and_locations():
    """Load locations from opp_json/*.json and org_json/*.json"""
    print 'load_opportunities_and_locations'

    dir = 'opp_html'
    listing = os.listdir(dir)
    for infile in listing:
        
        # extract opportunity id
        vm_id = infile.split('.')[0]
        print vm_id
        # some opportunitites were manually deleted
        try:
            data = json.loads(open(dir+'/'+infile).read())
        except:
            pass

        # get location's data
        lat = data['latitude']
        lng = data['longitude']
        try:
            st_add1 = data['street-address']
        except:
            st_add1 = ''
        try:
            st_add2 = data['street-address2']
        except:
            st_add2 = ''
        city = data['city']
        zip_code = data['zip_code']
        try:
            opp_time = data['opp_time']
        except:
            opp_time = ''

        opportunity = Opportunity(vm_id=vm_id,
                                  opp_time=opp_time)
        db.session.add(opportunity)
        db.session.commit()

        try:
            location = Loaction.query.filter_by(Location.lat == lat,
                                                Location.lng == lng,
                                                Location.st_add1 == st_add1,
                                                Location.st_add2 == st_add2,
                                                Location.city == city,
                                                Location.zip_code == zip_code).all()
            continue

        except:
            location = Location(lat=lat,
                                lng=lng,
                                st_add1=st_add1,
                                st_add2=st_add2,
                                city=city,
                                zip_code=zip_code)
            db.session.add(location)
            db.session.commit()

# ========= Update opportunities ==============================================
def update_opportunities():
    print 'update_opportunities' 

    for line in open('opportunities.json'):
        for opp in json.loads(line)['opportunities']:
            # Checking if this opp in in opportunitites table
            try:
                opportunity = Opportunity.query.filter_by(vm_id=opp['id']).one()

                opportunity.img_url = opp['imageUrl']
                opportunity.parent_place = opp['parentOrg']['id']
                opportunity.descr = opp['plaintextDescription']
                opportunity.title = opp['title']
                opportunity.tags = opp['tags']
                opportunity.categoryIds = opp['categoryIds']

                db.session.commit()
                print "opportunity updated"
            
            except:
                print 'Smth went wrong'
                continue          
                 
# ========= Category tables ===================================================
def load_categories():
    """Load categories from meta.json"""
    print 'load_categories'
    
    for cat in json.loads(open('meta.json').read())['categories']:
        vm_id = cat['id']
        category_name = cat['name']
        category = Category(vm_id=vm_id,
                            category_name=category_name)
        db.session.add(category)
        db.session.commit()
        print 'cdtegory committed'

def load_place_category():
    """load association table PlaceCategory from organizations.json"""
    print 'load_place_category'

    for line in open('organizations.json'):
        for org in json.loads(line)['organizations']:
            try:
                place = Place.query.filter_by(vm_id=org['id']).one()
                for i in range(len(org['categoryIds'])):
                    place_id = org['id']
                    category_id = org['categoryIds'][i]
                    placeCategory = PlaceCategory(place_id=place_id,
                                                  category_id =category_id)
                    db.session.add(placeCategory)
                    # try      
                    db.session.commit()
                    print 'place_category committed'

            except:
                print 'Smth went wrong'
                continue

def load_opportunity_category():
    """load association table OpportunityCategory from opportunities.json"""
    print 'load_opportunity_category'

    for line in open('opportunities.json'):
        for opp in json.loads(line)['opportunities']:
            try:
                opportunity = Opportunity.query.filter_by(vm_id=opp['id']).one()
                for i in range(len(opp['categoryIds'])):
                    opportunity_id = opp['id']
                    category_id = opp['categoryIds'][i]
                    opportunityCategory = OpportunityCategory(opportunity_id=opportunity_id,
                                                              category_id =category_id)
                    db.session.add(opportunityCategory)
                    db.session.commit()
                    print 'opportunity_category committed'
            except:
                print 'Smth went wrong'

# ========= Loaction tables ===================================================

def load_locations_for_places():
    dir = 'org_html'
    listing = os.listdir(dir)
    for infile in listing:
        # extract organization's id
        vm_id = int(infile.split('.')[0])
        data = json.loads(open(dir+'/'+infile).read())
        # get location's data
        lat = data['latitude']
        lng = data['longitude']

        try:
            location = Location.query.filter_by(lat=lat, lng=lng).first()
            place = Place.query.filter_by(vm_id=vm_id).one()
            # print location.location_id, place.vm_id
            place_location = PlaceLocation(place_id=place.vm_id,
                                           location_id=location.location_id)
            print 'place_location created'
            print place_location
            db.session.add(place_location)
            db.session.commit()
            print 'place_location committed'
        except:
            print 'Smth went wrong'



def load_locations_for_opportunities():
    dir = 'opp_html'
    listing = os.listdir(dir)
    for infile in listing:
        # extract opportunity id
        vm_id = infile.split('.')[0]
        try:
            data = json.loads(open(dir+'/'+infile).read())
        except:
            pass
        # get location's data
        lat = data['latitude']
        lng = data['longitude']

        try:
            location = Location.query.filter_by(lat=lat, lng=lng).first()
            opportunity = Opportunity.query.filter_by(vm_id=vm_id).one()
            opportunity_location = OpportunityLocation(opportunity_id=opportunity.vm_id,
                                                       location_id=location.location_id)
            print 'opportunity_location created'
            db.session.add(opportunity_location)
            db.session.commit()
            print 'committed'
        except:
            print 'Smth went wrong'



# =============================================================================

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.drop_all()
    db.create_all()

# ========= Seed all data =====================================================
    load_places_and_locations()
    update_places()
    load_opportunities_and_locations()
    update_opportunities()
    load_categories()
    load_place_category()
    load_opportunity_category()
    load_locations_for_places()
    load_locations_for_opportunities()

