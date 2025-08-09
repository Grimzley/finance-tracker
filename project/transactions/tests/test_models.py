from django.test import TestCase, Client
from django.contrib.auth.models import User
from transactions.models import Transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class TransactionModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.transaction = Transaction(user=self.user, title="Kbbq", amount=25.99, transaction_type="expense", category="food")

    def test_to_string(self):
        self.assertEqual(str(self.transaction), "expense: Kbbq ($25.99)")

    def test_get_category(self):
        self.assertEqual(self.transaction.get_category(), "Food")
    
    def test_category_validation(self):
        self.transaction.category = "salary"
        with self.assertRaises(ValidationError):
            self.transaction.clean()

    def test_negative_amount_contraint(self):
        self.transaction.amount = -1
        with self.assertRaises(IntegrityError):
            self.transaction.save()

    def test_large_amount_contraint(self):
        self.transaction.amount = 1_000_000.99
        with self.assertRaises(IntegrityError):
            self.transaction.save()
