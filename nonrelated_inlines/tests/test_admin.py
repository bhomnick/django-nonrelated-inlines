from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .testapp.models import Customer, Invoice


class TestAdmin(TestCase):

    def setUp(self):
        u = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        self.client.force_login(u)

    def test_can_view_related(self):
        Customer.objects.create(email='admin@example.com', name='admin')
        i = Invoice.objects.create(email='admin@example.com', amount=25)
        url = reverse('admin:testapp_customer_change', args=(i.pk,))

        res = self.client.get(url)
        self.assertEqual(res.context_data['inline_admin_formsets'][0].formset.forms[0].instance, i)

    def test_can_create_related(self):
        url = reverse('admin:testapp_customer_add')
        res = self.client.post(url, follow=True, data={
            'email': 'admin@example.com',
            'name': 'admin',
            'testapp-invoice-0-amount': 50,
            'testapp-invoice-INITIAL_FORMS': 0,
            'testapp-invoice-TOTAL_FORMS': 1
        })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.first().email, 'admin@example.com')

    def test_can_edit_related(self):
        Customer.objects.create(email='admin@example.com', name='admin')
        i = Invoice.objects.create(email='admin@example.com', amount=25)
        url = reverse('admin:testapp_customer_change', args=(i.pk,))

        res = self.client.post(url, follow=True, data={
            'email': 'admin@example.com',
            'name': 'admin',
            'testapp-invoice-0-id': i.id,
            'testapp-invoice-0-amount': 100,
            'testapp-invoice-INITIAL_FORMS': 1,
            'testapp-invoice-TOTAL_FORMS': 1
        })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.first().amount, 100)

    def test_can_delete_related(self):
        Customer.objects.create(email='admin@example.com', name='admin')
        i = Invoice.objects.create(email='admin@example.com', amount=25)
        url = reverse('admin:testapp_customer_change', args=(i.pk,))

        self.client.post(url, follow=True, data={
            'email': 'admin@example.com',
            'name': 'admin',
            'testapp-invoice-0-id': i.id,
            'testapp-invoice-0-DELETE': 'checked',
            'testapp-invoice-INITIAL_FORMS': 1,
            'testapp-invoice-TOTAL_FORMS': 1
        })

        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Invoice.objects.count(), 0)
