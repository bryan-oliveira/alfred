import unittest

from flask_testing import TestCase

from app import app


class TestTestingConfig(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_test(self):
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is False)


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is True)


class TestProductionConfig(TestCase):

    def create_app(self):
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is True)
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 13)


if __name__ == '__main__':
    unittest.main()
