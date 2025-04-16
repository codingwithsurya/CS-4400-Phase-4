from django.test import TestCase
from django.test import Client

# Create your tests here.
class Exercise1TestCase(TestCase):
    def test_admin_get(self):
        """
        Test that we can make a request, we use /admin since it's the only
        URL map set up by default. This at least lets us know Django is
        installed properly.
        """
        c = Client()
        response = c.get('/admin/')
        self.assertEqual(response.status_code, 302)