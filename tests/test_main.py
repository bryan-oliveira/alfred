import unittest

from util import BaseTestCase


class TestMainViews(BaseTestCase):

    def test_main_route_does_not_require_login(self):
        # Ensure main route requires a logged in user.
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed('categories.html')


if __name__ == '__main__':
    unittest.main()
