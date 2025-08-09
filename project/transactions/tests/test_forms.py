from django.test import TestCase, Client
from django.contrib.auth.models import User
from transactions.models import Transaction
from decimal import Decimal

class TransactionFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.transaction = Transaction.objects.create(user=self.user, title="Kbbq", amount=25.99, transaction_type="expense", category="food")

    def test_create_transaction_with_valid_form(self):
        self.client.force_login(self.user)
        form_data = {
            'title': 'Hotpot',
            'amount': '35.00',
            'transaction_type': 'expense',
            'category': 'food',
        }
        response = self.client.post('/transactions/add/', data=form_data)
        self.assertTrue(Transaction.objects.filter(title='Hotpot').exists())

    def test_dont_create_transaction_with_invalid_form(self):
        Transaction.objects.all().delete()
        self.client.force_login(self.user)
        form_data = {
            'title': '',
            'amount': '-25.99',
            'transaction_type': 'income',
            'category': 'food',
        }
        response = self.client.post('/transactions/add/', data=form_data)
        self.assertFalse(Transaction.objects.exists())

    def test_create_transaction_redirects_unauthenticated_user(self):
        form_data = {
            'title': 'Hotpot',
            'amount': '35.00',
            'transaction_type': 'expense',
            'category': 'food',
        }
        response = self.client.post('/transactions/add/', data=form_data)
        self.assertRedirects(response, expected_url="/login/?next=/transactions/add/")

    def test_edit_transaction(self):
        self.client.force_login(self.user)
        form_data = {
            'title': 'Thang Thang',
            'amount': '70.58',
            'transaction_type': 'expense',
            'category': 'food',
        }
        response = self.client.post(f'/transactions/{self.transaction.id}/edit/', data=form_data)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, 'Thang Thang')
        self.assertEqual(self.transaction.amount, Decimal("70.58"))

    def test_edit_transaction_redirects_unauthenticated_user(self):
        form_data = {
            'title': 'Thang Thang',
            'amount': '70.58',
            'transaction_type': 'expense',
            'category': 'food',
        }
        response = self.client.post(f'/transactions/{self.transaction.id}/edit/', data=form_data)
        self.assertRedirects(response, expected_url=f"/login/?next=/transactions/{self.transaction.id}/edit/")

    def test_delete_transaction(self):
        self.client.force_login(self.user)
        self.assertTrue(Transaction.objects.exists())
        response = self.client.post(f'/transactions/{self.transaction.id}/delete/')
        self.assertFalse(Transaction.objects.exists())

    def test_delete_transaction_redirects_unauthenticated_user(self):
        response = self.client.post(f'/transactions/{self.transaction.id}/delete/')
        self.assertRedirects(response, expected_url=f"/login/?next=/transactions/{self.transaction.id}/delete/")
