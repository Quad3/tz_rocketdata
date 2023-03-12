from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from datetime import datetime
from decimal import Decimal
import json

from .models import Producer, Contact, Address
from .views import ProducerAPIView


class ProducerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        address = Address.objects.create(
            country='Sup',
            city='A',
            street='First',
            house_number=123,
        )
        contact = Contact.objects.create(
            email='test@test.com',
            address=address,
        )
        Producer.objects.create(
            name='Amazon',
            debt=123.12,
            level=0,
            contact=contact,
        )
    
    def test_producer_data(self):
        producer = Producer.objects.get(pk=1)
        
        self.assertEquals(producer.name, 'Amazon')
        self.assertEquals(producer.debt, Decimal((0, (1, 2, 3, 1, 2), -2)))
        self.assertEquals(float(producer.debt), 123.12)
        self.assertEquals(producer.level, 0)
        self.assertEquals(producer.provider, None)
        self.assertEquals(producer.contact.email, 'test@test.com')
        self.assertEquals(producer.contact.address.country, 'Sup')
        self.assertEquals(producer.contact.address.city, 'A')
        self.assertEquals(producer.contact.address.street, 'First')
        self.assertEquals(producer.contact.address.house_number, 123)
        self.assertEquals(type(producer.created_at), datetime)


class ProducerAPIViewTest(TestCase):

    def test_post_request(self):
        factory = APIRequestFactory()
        view = ProducerAPIView.as_view()
        data = {
            'name': 'Apple',
            'debt': 123.45,
            'contact': {
                'email': 'email@email.com',
                'address': {
                    'country': 'Newland',
                    'city': 'Q',
                    'street': 'Second',
                    'house_number': 333,
                },
            },
        }
        post_request = factory.post(
            path='api/v1/producer',
            data=json.dumps(data),
            content_type='application/json',
        )
        post_response = view(post_request)
        
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(post_response.data['name'], 'Apple')
        self.assertEquals(float(post_response.data['debt']), 123.45)
        self.assertEquals(post_response.data['level'], 0)
        self.assertEquals(post_response.data['contact']['email'], 'email@email.com')
        self.assertEquals(post_response.data['contact']['address']['country'], 'Newland')
        self.assertEquals(post_response.data['contact']['address']['city'], 'Q')
        self.assertEquals(post_response.data['contact']['address']['house_number'], 333)
        self.assertEquals(post_response.data['contact']['address']['street'], 'Second')

    def test_get_request(self):
        factory = APIRequestFactory()
        view = ProducerAPIView.as_view()
        get_request = factory.get('api/v1/producer')
        get_response = view(get_request)

        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(get_response.data), 0)
