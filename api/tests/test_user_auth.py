import unittest

from requests.auth import _basic_auth_str


from api.app.config import TestingConfig
from api.app import create_app, db


class UserAuthTestCase(unittest.TestCase):
    """This class represents the business test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig())
        self.client = self.app.test_client

        self.user1 = {
            'name': 'John Doe',
            'email': 'john.doe@mail.com',
            'password': 'password',
            'type': 'customer',

        }
        self.user2 = {
            'name': 'John Doe',
            'email': 'john.doe@mail.com',
            'password': 'password',
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        # Register user
        res = self.client().post("/auth/registration", json=self.user1)
        self.assertEqual(200, res.status_code)

    def test_user_login(self):
        # Register user
        res = self.client().post("/auth/registration", json=self.user1)
        self.assertEqual(200, res.status_code)

        # Login user
        headers = {'Authorization': _basic_auth_str(
            self.user1.get("email"),
            self.user1.get("password"))
        }
        res = self.client().post("/auth/login", headers=headers)
        self.assertEqual(200, res.status_code)

    def test_user_refresh(self):
        # Register user
        res = self.client().post("/auth/registration", json=self.user1)
        self.assertEqual(200, res.status_code)

        # Login user
        headers = {'Authorization': _basic_auth_str(
            self.user1.get("email"),
            self.user1.get("password"))
        }
        res = self.client().post("/auth/login", headers=headers)
        self.assertEqual(200, res.status_code)
        refresh_token = res.json.get("refresh_token")

        # Refresh user
        headers = {'Authorization': 'Bearer {token}'.format(token=refresh_token)}
        res = self.client().post("/auth/token/refresh", headers=headers, content_type="application/json")
        self.assertEqual(200, res.status_code)

    def test_user_logout_refresh(self):
        # Register user
        res = self.client().post("/auth/registration", json=self.user1)
        self.assertEqual(200, res.status_code)

        # Login user
        headers = {'Authorization': _basic_auth_str(
            self.user1.get("email"),
            self.user1.get("password"))
        }
        res = self.client().post("/auth/login", headers=headers)
        self.assertEqual(200, res.status_code)
        refresh_token = res.json.get("refresh_token")

        # Logout refresh user
        headers = {'Authorization': 'Bearer {token}'.format(token=refresh_token)}
        res = self.client().post("/auth/logout/refresh", headers=headers, content_type="application/json")
        self.assertEqual(200, res.status_code)
        self.assertIn("Refresh token has been revoked", str(res.data))

    def test_user_logout_access(self):
        # Register user
        res = self.client().post("/auth/registration", json=self.user1)
        self.assertEqual(200, res.status_code)

        # Login user
        headers = {'Authorization': _basic_auth_str(
            self.user1.get("email"),
            self.user1.get("password"))
        }
        res = self.client().post("/auth/login", headers=headers)
        self.assertEqual(200, res.status_code)
        access_token = res.json.get("access_token")

        # Logout access user
        headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        res = self.client().post("/auth/logout/access", headers=headers, content_type="application/json")
        self.assertEqual(200, res.status_code)
        self.assertIn("Access token has been revoked", str(res.data))
