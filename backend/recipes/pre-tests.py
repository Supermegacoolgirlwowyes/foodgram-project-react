from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class UsersTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.main_user = User.objects.create_user(
            username='main_user',
            email='main_user@mail.com',
            password='Main_User_Password',
        )
        self.additional_user = User.objects.create_user(
            username='additional_user',
            email='additional_user@mail.com',
            password='Additional_User_Password',
        )
        self.client_main = APIClient()
        self.client_main.force_authenticate(user=self.main_user)
        self.client_additional = APIClient()
        self.client_additional.force_authenticate(user=self.additional_user)

        Ingredient.objects.create(name='пицца', measurement_unit='шт')
        Tag.objects.create(name='завтрак', color='#123456', slug='breakfast')

    def create_recipe(self):
        recipe = self.client_main.post(
            '/api/recipes/', {
                "ingredients": [
                    {
                        "id": 1832,
                        "amount": 1
                    },
                    {
                        "id": 1860,
                        "amount": 70
                    },
                    {
                        "id": 1077,
                        "amount": 200
                    },
                ],
                "tags": [2, 3 ],
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA"
                         "AgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAA"
                         "DklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
                "name": "Пицца",
                "text": "Описание приготовления",
                "cooking_time": 30
            }
        )
        return recipe

    def test_create_recipe(self):
        response = self.client.post(
            '/api/recipes/', {
                "ingredients": [
                    { "id": 1, "amount": 1 }
                ],
                "tags": [1],
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAyAEsDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9EKKKKACipLKzm1K/gtbeMy3F1KkMSAgF3ZgqrzxySBzxzXXXnwXm0+6kt7jxZ8P4LiFzHLFJrRV43U4ZWHlcEEEEdiKAONorrf8AhUf/AFOPw7/8HZ/+NUf8Kj/6nH4d/wDg7P8A8aoA5Kitrxh4Eu/BcdjLNdaVqFpqSSNbXWnXX2iCUxtsdQ2AcqxAPGMnGcggYtABRRRQAUUUUAa3w+/5KH4d/wCwtZ/+j0r1LwH4h8DaP4q8dR+KoLF719dvHjkurM3CmASt8qfK2GDbyQACcr1xx5b8Pv8Akofh3/sLWf8A6PSvX/hB8ILDxr8S/FmvakwuIdN8RXtvDaMvyPKspfe/qBvXC+oOc8CgDx3RvDVx448Wf2foNnNIbqVzbxO2TDFu4MjcgBVIy3r0ySAev+Lv7PmofDDTLfUI5v7SsNirdSqm37NL3yP+eZPRj06HsT9GeEvhzongS4vpdJsobOTUpfNmK/oq/wB1ByQowoLHAFbVzDHeQtFIqSRyAq6MAyuDwQR3BoA+RfGP/JHPh/8A9xb/ANKxXI11ni0/8WX+Hv01X/0rWuToAKKKKACiiigCbTdQm0fVLW8t2VbizmS4iLLuAdGDKSO/IHFddqXxP0PWb+a7vPAehXN3dSNNNKbmUeY7EszY7ZYk4964uigDrf8AhPPDP/RPNB/8CpaP+E88M/8ARPNB/wDAqWuSooA3vG3jr/hL7XTbWDTbPSdP0lJVtra3LNtMrh5CWY5OWAPbHPrWDRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB//Z",
                "name": "Пицца",
                "text": "Описание приготовления",
                "cooking_time": 30
            }
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)

        """with self.subTest(response=response):
            self.assertEqual(
                response.status_code,
                201,
                "Make sure new recipe can be created"
            )
        with self.subTest(response=response):
            self.assertEqual(
                Recipe.objects.all().count(),
                1,
                "Make sure a recipe had been added to a database"
            )"""

        """recipe = User.objects.get(username=self.user.username)

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
        )"""



    """def test_delete_recipe(self):
        response = self.create_recipe()
        self.assertEqual(response.status_code, 201, 'Recipe created')

        response = self.client_main_user.get('/api/recipes/1')
        response = Recipe.objects.all().count()
        self.assertEqual(response, 1, 'Recipe found')

        response = self.client.delete('/api/recipes/1/')
        self.assertEqual(
            response.status_code,
            401,
            'Unauthorized user cannot delete recipes'
        )
        response = self.client_main_user.delete('/api/recipes/2/')
        self.assertEqual(
            response.status_code,
            404,
            'Recipe to delete is not found'
        )
        response = self.client_main_user.delete('/api/recipes/1/')
        self.assertEqual(
            response.status_code,
            204,
            'Recipe was successfully deleted'
        )"""
