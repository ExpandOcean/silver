import json

from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from silver.tests.factories import (AdminUserFactory, CustomerFactory,
                                    ProviderFactory)


class TestProformaEndpoints(APITestCase):
    def setUp(self):
        admin_user = AdminUserFactory.create()
        self.client.force_authenticate(user=admin_user)

    def test_post_proforma_without_proforma_entries(self):
        CustomerFactory.create()
        ProviderFactory.create()
        url = reverse('proforma-list')

        data = {
            'provider': 'http://testserver/providers/1/',
            'customer': 'http://testserver/customers/1/',
            'number': "",
            'currency': 'RON',
            'proforma_entries': []
        }

        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
            "id": 1,
            "series": "ProformaSeries",
            "number": 1,
            "provider": "http://testserver/providers/1/",
            "customer": "http://testserver/customers/1/",
            "archived_provider": {},
            "archived_customer": {},
            "due_date": None,
            "issue_date": None,
            "paid_date": None,
            "cancel_date": None,
            "sales_tax_name": "VAT",
            "sales_tax_percent": '1.00',
            "currency": "RON",
            "state": "draft",
            "invoice": None,
            "proforma_entries": []
        }

    def test_post_proforma_with_proforma_entries(self):
        CustomerFactory.create()
        ProviderFactory.create()
        url = reverse('proforma-list')
        data = {
            'provider': 'http://testserver/providers/1/',
            'customer': 'http://testserver/customers/1/',
            'number': None,
            'currency': 'RON',
            'proforma_entries': [{
                "description": "Page views",
                "unit_price": 10.0,
                "quantity": 20
            }]
        }

        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED
        # TODO: Check the body of the response. There were some problems
        # related to the invoice_entries list.
