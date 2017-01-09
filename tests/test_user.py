from app.forms import RegisterForm, LoginForm, DeleteForm, ProfileForm

from util import BaseTestCase
from flask_login import current_user
from app.models import User


class TestUserForms(BaseTestCase):

    def test_validate_success_register_form(self):
        # Ensure correct user data validates
        form = RegisterForm(
            fullname="Test User",
            username="testuser",
            email="testx@test.com",
            password="123123",
            password_conf="123123",
            age=100,
            gender="M")
        # print "--", form.errors
        self.assertTrue(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register with a duplicate email
        form = RegisterForm(
            fullname="Test User",
            username="testuser",
            email="test@test.com",
            password="123123",
            age=100,
            gender="M"
        )
        self.assertFalse(form.validate())

    def test_validate_success_login_form(self):
        # Ensure correct login data validates
        form = LoginForm(username='testuser', password='123123', remember_me=False)
        self.assertTrue(form.validate())

    def test_invalid_email_format(self):
        # Ensure invalid email format throws error
        form = RegisterForm(
            fullname="Test User",
            username="testuser",
            email="invalid-email",
            password="123123",
            age=100,
            gender="M"
        )
        self.assertFalse(form.validate())

    def test_validate_success_email_format(self):
        # Ensure invalid email format throws error
        form = RegisterForm(
            fullname="Test User",
            username="testuser",
            email="test@test.com",
            password="123123",
            age=100,
            gender="M"
        )
        self.assertFalse(form.validate())

    def test_validate_success_delete_account_form(self):
        # Ensure correct account delete form validates
        form = DeleteForm(password='123123')
        self.assertTrue(form.validate())

    def test_invalid_delete_account_form(self):
        # Ensure invalid data on account deletion throws error
        form = DeleteForm(password='')
        self.assertFalse(form.validate())

    def test_validate_success_profile_form(self):
        # Ensure correct profile info validates
        form = ProfileForm(
            fullname='Test User',
            username='testuser',
            email='test@test.com',
            gender='M',
            age=100
        )
        self.assertTrue(form.validate())

    def test_invalid_profile_form(self):
        # Ensure correct profile info validates
        form = ProfileForm(
            fullname='',
            username='testuser',
            email='test@test.com',
            gender='M',
            age=100
        )
        # Require name
        self.assertFalse(form.validate())

        # Require username
        form.fullname = 'Test User'
        form.username = ''
        self.assertFalse(form.validate())

        # Require email
        form.username = 'testuser'
        form.email = ''
        self.assertFalse(form.validate())

        # Require age
        form.email = 'test@test.com'
        form.age = ''
        self.assertFalse(form.validate())


class TestUserViews(BaseTestCase):

    def test_main_route_does_not_require_login(self):
        # Ensure main route requires a logged in user.
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed('categories.html')

    def test_correct_login(self):
        # Ensure correct login data validates
        with self.client:
            response = self.client.post('/login', data=dict(username='testuser',
                                                            password='123123',
                                                            ), follow_redirects=True)
            self.assertTrue(response.status_code == 200)
            self.assertTrue(current_user.email == "test@test.com")
            self.assertTrue(current_user.is_authenticated)
            self.assertTemplateUsed('categories.html')
            assert 'Logged in successfully!' in response.data

    def test_incorrect_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='xxxxxx',
        ), follow_redirects=True)
        assert 'Invalid username/password.' in response.data

    def test_favorites_view_is_empty(self):
        # Ensure correct login data validates
        with self.client:

            # Login user
            self.client.post('/login', data=dict(username='testuser',
                                                 password='123123',
                                                 ), follow_redirects=True)
            # Check favorites
            response = self.client.get('/favorites', follow_redirects=True)

            self.assertTrue(response.status_code == 200)
            self.assertTemplateUsed('favorites.html')

    def test_require_login_to_view_favorites(self):
        # Ensure correct login data validates
        with self.client:
            response = self.client.get('/favorites', follow_redirects=True)
            assert 'Please log in to view favorites.' in response.data
            self.assertTrue(response.status_code == 200)
            self.assertTemplateUsed('categories.html')

    def test_view_profile(self):
        # Ensure correct login data validates
        with self.client:
            # Login user
            self.client.post('/login', data=dict(username='testuser',
                                                 password='123123',
                                                 ), follow_redirects=True)
            # Check Profile
            response = self.client.get('/profile', follow_redirects=True)

            self.assertTrue(response.status_code == 200)
            self.assertTemplateUsed('profile.html')

    def test_require_login_to_view_profile(self):
        # Ensure correct login data validates
        with self.client:
            response = self.client.get('/profile', follow_redirects=True)
            assert 'Please log in to view profile.' in response.data
            self.assertTrue(response.status_code == 200)
            self.assertTemplateUsed('categories.html')
