from events.models import models
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

class YearTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {}