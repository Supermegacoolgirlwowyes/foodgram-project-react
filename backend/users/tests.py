from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UsersTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="auth_user",
            email="auth_user@mail.com",
            password="User_Password",
        )
        self.client_auth = APIClient()
        self.client_auth.force_authenticate(user=self.user)

    def get_token(self):
        return self.client.post(
            "/api/auth/token/login/", {
                "email": "auth_user@mail.com",
                "password": "User_Password",
            },
        )

    def create_user(self):
        return self.client.post(
            "/api/users/", {
                "username": "test_username",
                "email": "testusername@mail.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "test_password",
            }
        )

    def test_create_user(self):
        response = self.create_user()
        self.assertEqual(
            response.status_code,
            201,
            "Make sure new user can be created"
        )
        user = User.objects.get(username=self.user.username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        response = self.client.post(
            "/api/users/", {
                "username": "test_username",
            }
        )
        self.assertEqual(
            response.status_code,
            400,
            "Make sure new user cannot be created without "
            "providing requiered information"
        )
        self.assertEqual(
            User.objects.all().count(),
            2,
            "Make sure only one user has been created with request"
        )

    def test_get_all_users(self):
        self.create_user()
        response = self.client.get("/api/users/")
        self.assertEqual(
            response.status_code,
            200,
            "Make sure /api/users/ is available"
        )

        response = response.json()
        self.assertEqual(
            response['count'],
            2,
            "Make sure all users are listed"
        )

    def test_get_user_by_id(self):
        response = self.client.get("/api/users/1/")
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                401,
                "Make sure unauthenticated user cannot access user by it's ID"
            )

        response = self.client_auth.get("/api/users/1/")
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                200,
                "Make sure authenticated user can access user by it's ID"
            )

        model_fields = [
            "email",
            "first_name",
            "last_name",
            "id",
            "username",
            "is_subscribed"
        ]
        for field in model_fields:
            with self.subTest(field=field):
                self.assertTrue(
                    field in response.data.keys(),
                    f"Make sure field: '{field}' is listed"
                )

        with self.subTest(response=response):
            self.assertFalse(
                "password" in response.data.keys(),
                "Make sure field: 'password' doesn't appear in response"
            )

        response = self.client_auth.get("/api/users/666/")
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                404,
                "Make sure HTTP_404_NOT_FOUND returned "
                "if requested user doesn't exist"
            )

    def test_me(self):

        response = self.client.get("/api/users/me/")
        self.assertEqual(
            response.status_code,
            401,
            "Make sure only authenticated users can "
            "retreive information about themselves"
        )

        response = self.client_auth.get("/api/users/me/")
        self.assertEqual(
            response.status_code,
            200,
            "Make sure authenticated users can "
            "retreive information about themselves"
        )

    def test_set_password(self):
        current_password = "User_Password"
        new_password = "New_User_Password"

        response = self.client.post(
            "/api/users/set_password/", {
                "current_password": current_password,
                "new_password": new_password
            }
        )
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                401,
                "Make sure unauthenticated users are "
                "not authorized to change password"
            )

        response = self.client_auth.post(
            "/api/users/set_password/", {
                "current_password": "auth_user_password",
                "new_password": new_password
            }
        )
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                400,
                "Make sure authenticated users cannot change their "
                "password without providing correct current_password"
            )

        response = self.client_auth.post(
            "/api/users/set_password/", {
                "current_password": current_password,
                "new_password": new_password
            }
        )
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                204,
                "Make sure users can successfuly change their passwords"
            )

    def test_login(self):
        response = self.client.post(
            "/api/auth/token/login/", {
                "email": "auth_user@mail.com",
                "password": "User_password",
            },
        )
        with self.subTest(response=response):
            self.assertEquals(
                response.status_code,
                400,
                "Make sure Token is not generated with wrong user credentials"
            )

        response = self.get_token()
        with self.subTest(response=response):
            self.assertEquals(
                response.status_code,
                200,
                "Make sure Token generating request is sucessful"
            )
        with self.subTest(response=response):
            self.assertTrue(
                "auth_token" in response.data.keys(),
                "Make sure Token is provided with correct user credentials"
            )

    def test_logout(self):
        response = self.get_token()
        token_1 = response.data["auth_token"]

        response = self.client.post(
            "/api/auth/token/logout/",
            HTTP_AUTHORIZATION="Token " + token_1
        )
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                204,
                "Make sure authenticated user can successfully logout"
            )

        response = self.get_token()
        token_2 = response.data["auth_token"]

        with self.subTest(token_1=token_1, token_2=token_2):
            self.assertNotEqual(
                token_1,
                token_2,
                "Make sure new token is different from the previous one"
            )

        response = self.client.post(
            "/api/auth/token/logout/",
            HTTP_AUTHORIZATION="Token " + token_1
        )
        with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                401,
                "Make sure users cannot use their previous tokens"
            )
