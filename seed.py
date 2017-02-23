from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
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
import json




def load_places_and_locations():
    """Load locations from opp_json/*.json and org_json/*.json"""

    print 'load_places_and_locations'
    
    Place.query.delete()
    # Location.query.delete()

    dir = 'org_json'
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

        loc = db.session.query(Location.location_id).filter(Location.vm_id == vm_id).all()

        # if vm_id == 315384:
        #     print lat
        #     print lng
        #     print loc

        if not loc:
            location = Location(lat=lat,
                            lng=lng,
                            st_add1=st_add1,
                            st_add2=st_add2,
                            city=city,
                            zip_code=zip_code,
                            vm_id = vm_id)
            db.session.add(location)


    for line in open('organizations.json'):
         for org in json.loads(line)['organizations']:
            name = org['name']
            place_type = org['type']
            img_url = org['imageUrl']
            descr = org['description']
            
            try:
                location = Location.query.filter_by(vm_id=org['id']).one()
                place = Place(vm_id = org['id'],
                            name = name,
                            place_type = place_type,
                            img_url = img_url,
                            descr = descr,
                            location = location)

            except NoResultFound:
                print org['id'], 'not found'
                continue

            print place
            db.session.add(place)
            print "place added"
            db.session.commit()
            print "place commited"

            

def load_opportunities_and_locations():
    """Load locations from opp_json/*.json and org_json/*.json"""
    print 'load_opportunities_and_locations'

    dir = 'opp_json'
    listing = os.listdir(dir)
    for infile in listing:
        
        # extract opportunity id
        vm_id = infile.split('.')[0]
        print vm_id
        try:
            data = json.loads(open(dir+'/'+infile).read())
        except Exception:
            print vm_id, 'no longer available'
            continue

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

        loc = db.session.query(Location.location_id).filter(Location.vm_id == vm_id).all()

        if not loc:
            location = Location(lat=lat,
                            lng=lng,
                            st_add1=st_add1,
                            st_add2=st_add2,
                            city=city,
                            zip_code=zip_code,
                            vm_id = vm_id)
            db.session.add(location)
            db.session.commit()
            loc = db.session.query(Location.location_id).filter(Location.lat == lat, Location.lng == lng).all()
        # validate data type
        # descr = data['description']
        # title = data['title']

        opp_time = data['opp_time']
        opp_type = data['opp_type']

        opp = db.session.query(Opportunity.vm_id).filter(Opportunity.vm_id == vm_id).all()

        if not opp:
            opp = Opportunity(vm_id=vm_id,
                              opp_time=opp_time,
                              opp_type=opp_type,
                              location=location)
            db.session.add(opp)
            db.session.commit()
    print "OPEN OPPORTUNITIES.JSON"    

    for line in open('opportunities.json'):
        for opp in json.loads(line)['opportunities']:
            try:
                cur_opp = Opportunity.query.filter_by(vm_id=opp['id']).first()
                cur_opp.img_url = opp['imageUrl']
                cur_opp.parent_place = opp['parentOrg']['id']
                cur_opp.descr = opp['plaintextDescription']
                cur_opp.title = opp['title']
                cur_opp.availability = json.dumps(opp['availability'])
    
                db.session.add(cur_opp)
                print 'opp added'
                print cur_opp
                db.session.commit()
                print 'opp commited'
            except:
                print 'was not commited opp:', opp['id'], 'parentOrg', opp['parentOrg']['id']
                continue
            


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
    print "seeded load_categories"


def load_place_category():
    """load association table PlaceCategory from organizations.json"""
    print 'load_place_category'

    f = open('organizations.json')

    for line in f:
        for org in json.loads(line)['organizations']:
            for i in range(len(org['categoryIds'])):
                place_id = org['id']
                category_id = org['categoryIds'][i]
                placeCategory = PlaceCategory(place_id=place_id,
                                              category_id =category_id)
                db.session.add(placeCategory)
                # try      
                db.session.commit()
                # except:
                #     continue


def load_opportunity_category():
    """load association table OpportunityCategory from opportunities.json"""
    print 'load_opportunity_category'

    for line in open('opportunities.json'):
        for opp in json.loads(line)['opportunities']:
            for i in range(len(opp['categoryIds'])):
                opportunity_id = opp['id']
                category_id = opp['categoryIds'][i]
                opportunityCategory = OpportunityCategory(opportunity_id=opportunity_id,
                                                          category_id =category_id)
                db.session.add(opportunityCategory)
                db.session.commit()
    print 'opportunity_category loaded'






# ----------------------------------------------------------------

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.drop_all()
    db.create_all()

    # Import different types of data
    # load_places_and_locations()
    # load_opportunities_and_locations()
    # load_categories()
    load_place_category()
    # load_opportunity_category()
