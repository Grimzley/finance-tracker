from django.test import TestCase, Client
from django.contrib.auth.models import User
from transactions.models import Transaction

class TransactionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Transaction.objects.create(user=self.user, title="Kbbq", amount=25.99, transaction_type="expense", category="food")

    def test_transaction_list_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get('/transactions/')
        self.assertTemplateUsed(response, 'transaction_list.html')

    def test_transaction_list_contains_title(self):
        self.client.force_login(self.user)
        response = self.client.get('/transactions/')
        self.assertContains(response, 'My Transactions', status_code=200)

    def test_transaction_list_redirects_unauthenticated_user(self):
        response = self.client.get('/transactions/')
        self.assertRedirects(response, expected_url="/login/?next=/transactions/")

    def test_transaction_list_context(self):
        self.client.force_login(self.user)
        response = self.client.get('/transactions/')
        self.assertEqual(len(response.context['transactions']), 1)
        self.assertContains(response, "Kbbq")
        self.assertNotContains(response, "Add a Transaction to Get Started!")

    def test_transaction_list_empty(self):
        self.client.force_login(self.user)
        Transaction.objects.all().delete()
        response = self.client.get('/transactions/')
        self.assertEqual(len(response.context['transactions']), 0)
        self.assertContains(response, "Add a Transaction to Get Started!")
