import unittest
# import testing.postgresql
from server import app
from model import db


class DataTests(unittest.TestCase):
    """Tests for database"""

    def setUp(self):
        """Set up database for testing purposes"""
        print "Setting up test database"
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = app
        db.init_app(app)
        db.create_all()


    def _create_place(self):

        # vm_id = db.Column(db.Integer, nullable=False, primary_key=True) # vm_id for easy access urls
        # name = db.Column(db.Text, nullable=True)
        # place_type = db.Column(db.Text, nullable=True)
        # img_url = db.Column(db.Text, nullable=True)
        # descr = db.Column(db.Text, nullable=True)
        # categoryIds = db.Column(db.Text, nullable=True)
        # mission = db.Column(db.Text, nullable=True)
        place = Place(vm_id='111111', name='Test place', descr='test description', categoryIds='25', mission='help help help')
        db.session.add(place)
        db.session.commit()

    # def test_place(self):

    #     place = Place(vm_id='111222', name='Test place', descr='test description', categoryIds='25', mission='help help help')
    #     db.session.add(place)
    #     db.session.commit()
    #     self.assertEqual(place.vm_id, '111222')
    #     # db.session.rollback()


    # def _create_opportunity(self):
    
    #     opportunity = Opportunty(vm_id='333', parent_place='111111', descr='helphelphelp', title='help someone now', tags='kids', categoryIds='17')
    #     db.session.add(opportunity)
    #     db.session.commit()

    def tearDown(self):
        """Remove testing db"""
        db.session.remove()
        db.drop_all()
        print "teardown ran"



class FlaskTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    
    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn('How can you help?', result.data)



    # def test_places(self):
    #     result = self.client.get('/places')
    #     self.assertIn('Places', result.data)




if __name__ == '__main__':

    unittest.main()