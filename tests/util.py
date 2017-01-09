from flask.ext.testing import TestCase

from app import app, db
from app.models import User, Favorite, Allergy


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    @classmethod
    def setUpClass(self):
        db.create_all()
        # Create user
        user = User(
            fullname="Test User",
            username="testuser",
            email="test@test.com",
            password="123123",
            age=100,
            gender="M"
        )

        # Test allergy obj
        al = Allergy()
        user.allergy = al

        db.session.add(user)
        db.session.add(al)
        db.session.commit()

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()
