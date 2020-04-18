import json
import unittest

from requests.auth import _basic_auth_str

from app import create_app, db
from app.businesses.models import User, Role
from app.config import TestingConfig


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client

        self.user1 = User.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@mail.com",
            password="password",
            role=Role.TYPE_ADMIN
        )
        self.user2 = User.create_user(
            first_name="Bobby",
            last_name="Pendragon",
            email="bobby.pendragon@mail.com",
            password="password",
            role=Role.TYPE_ADMIN
        )
        self.user3 = {
            'first_name': 'Johnny ',
            'last_name': 'Storm',
            'email': 'johnny.storm@mail.com',
            'password': 'password',
            'role': 'admin',
        }
        admin_role = Role(type="admin")
        # binds the app to the current context
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(admin_role)
            db.session.commit()

            for model in [self.user1, self.user2]:
                db.session.add(model)
            db.session.commit()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_put(self):
        res = self.client().put('/api_v1/users/1',
                                json={"first_name": "Ash", "last_name": "Ketchum", "email": "ask.ketchum@mail.com",
                                      "role": "admin", "active": True})
        self.assertIn('Ash', res.json.get("first_name"))
        self.assertIn('Ketchum', res.json.get("last_name"))
        self.assertEqual(200, res.status_code)

    def test_user_get_scalar(self):
        res = self.client().get('/api_v1/users/1')
        self.assertIn('John', res.json.get("first_name"))

    def test_user_get_collection(self):
        res = self.client().get('/api_v1/users')
        self.assertIn('John', res.json[0].get("first_name"))
        self.assertIn('Bobby', res.json[1].get("first_name"))

    def test_user_delete(self):
        res = self.client().delete('/api_v1/users/1')
        self.assertEqual(res.status_code, 204)

    def test_user_registration(self):
        res = self.client().post("/api_v1/auth/register",
                                 json=self.user3)
        self.assertEqual(201, res.status_code)

    def test_user_login(self):
        headers = {'Authorization': _basic_auth_str(
            "john.doe@mail.com",
            "password")
        }
        res = self.client().post("/api_v1/auth/login", headers=headers)
        self.assertEqual(200, res.status_code)

    def test_user_logout_refresh(self):
        headers = {'Authorization': _basic_auth_str(
            "john.doe@mail.com",
            "password")
        }
        res = self.client().post("/api_v1/auth/login", headers=headers)
        refresh_token = res.json.get("refresh_token")

        # Logout refresh user
        headers = {'Authorization': 'Bearer {token}'.format(token=refresh_token)}
        res = self.client().post("api_v1/auth/logout/refresh", headers=headers, content_type="application/json")
        self.assertEqual(200, res.status_code)
        self.assertIn("Refresh token has been revoked", res.json.get("message"))

    def test_user_logout_access(self):
        headers = {'Authorization': _basic_auth_str(
            "john.doe@mail.com",
            "password")
        }
        res = self.client().post("/api_v1/auth/login", headers=headers)
        access_token = res.json.get("access_token")

        # Logout refresh user
        headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        res = self.client().post("api_v1/auth/logout/access", headers=headers, content_type="application/json")
        self.assertEqual(200, res.status_code)
        self.assertIn("Access token has been revoked", res.json.get("message"))

    def test_user_token_refresh(self):
        headers = {'Authorization': _basic_auth_str(
            "john.doe@mail.com",
            "password")
        }
        res = self.client().post("/api_v1/auth/login", headers=headers)
        refresh_token1 = res.json.get("refresh_token")

        headers = {'Authorization': 'Bearer {token}'.format(token=refresh_token1)}
        res = self.client().post("api_v1/auth/token/refresh", headers=headers, content_type="application/json")
        self.assertNotEqual(refresh_token1, res.json.get("refresh_token"))
