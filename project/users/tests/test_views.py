from django.test import TestCase, Client
from django.contrib.auth.models import User
from transactions.models import Transaction

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_uses_correct_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'landing.html')

    def test_register_contains_title(self):
        response = self.client.get('/register/')
        self.assertContains(response, 'Register', status_code=200)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_uses_correct_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'landing.html')

    def test_login_contains_title(self):
        response = self.client.get('/login/')
        self.assertContains(response, 'Login', status_code=200)

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_logout_user(self):
        self.client.force_login(self.user)
        response = self.client.post('/logout/', follow=True)
        self.assertTemplateUsed(response, 'landing.html')
        self.assertNotIn("_auth_user_id", self.client.session)

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Transaction.objects.create(user=self.user, title="Kbbq", amount=50, transaction_type="expense", category="food")
        Transaction.objects.create(user=self.user, title="Paycheck", amount=500, transaction_type="income", category="salary")

    def test_dashboard_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_contains_title(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertContains(response, 'Dashboard Overview', status_code=200)

    def test_dashboard_redirects_unauthenticated_user(self):
        response = self.client.get('/')
        self.assertRedirects(response, expected_url="/login/?next=/")

    def test_transaction_list_context(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(len(response.context['recent']), 2)
        self.assertContains(response, "Kbbq")
        self.assertContains(response, "Paycheck")
        self.assertContains(response, "$450.00")

class SettingsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_settings_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get('/settings/')
        self.assertTemplateUsed(response, 'settings.html')

    def test_settings_contains_title(self):
        self.client.force_login(self.user)
        response = self.client.get('/settings/')
        self.assertContains(response, 'Settings', status_code=200)
    
    def test_settings_redirects_unauthenticated_user(self):
        response = self.client.get('/settings/')
        self.assertRedirects(response, expected_url="/login/?next=/settings/")
