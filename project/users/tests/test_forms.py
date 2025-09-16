from django.test import TestCase, Client
from django.contrib.auth.models import User

class RegisterFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.form_data = {
            'username': 'myuser',
            'password': 'myPassword1',
            'password_confirm': 'myPassword1'
        }

    def test_register_user_with_valid_form(self):
        response = self.client.post('/register/', data=self.form_data, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertTrue(User.objects.filter(username="myuser").exists())
        self.assertEqual(User.objects.count(), 2)
    
    def test_dont_register_user_already_exists(self):
        self.form_data['username'] = 'testuser'
        response = self.client.post('/register/', data=self.form_data)
        self.assertContains(response, 'A user with that username already exists.', status_code=200)
        self.assertEqual(User.objects.count(), 1)

    def test_dont_register_user_with_password_mismatch(self):
        self.form_data['password_confirm'] = 'myBassword2'
        response = self.client.post('/register/', data=self.form_data)
        self.assertContains(response, 'Passwords do not match!', status_code=200)
        self.assertFalse(User.objects.filter(username="myuser").exists())
        self.assertEqual(User.objects.count(), 1)
    
    def test_dont_register_user_with_bad_username_length(self):
        self.form_data['username'] = 'user'
        response = self.client.post('/register/', data=self.form_data)
        self.assertContains(response, 'Username must be at least 5 characters long.', status_code=200)
        self.assertFalse(User.objects.filter(username="user").exists())
        self.assertEqual(User.objects.count(), 1)

    def test_dont_register_user_with_bad_username_chars(self):
        self.form_data['username'] = 'myu$ername*'
        response = self.client.post('/register/', data=self.form_data)
        self.assertContains(response, 'Username can only contain letters, numbers, and underscores.', status_code=200)
        self.assertFalse(User.objects.filter(username="myu$ername*").exists())
        self.assertEqual(User.objects.count(), 1)

    def test_dont_register_user_with_bad_password_length(self):
        self.form_data['password'] = 'myPass1'
        self.form_data['password_confirm'] = 'myPass1'
        response = self.client.post('/register/', data=self.form_data)
        self.assertContains(response, 'Password must be at least 8 characters long.', status_code=200)
        self.assertFalse(User.objects.filter(username="myuser").exists())
        self.assertEqual(User.objects.count(), 1)
    
    def test_dont_register_user_with_bad_password_digit(self):
        self.form_data['password'] = 'myPassword'
        self.form_data['password_confirm'] = 'myPassword'
        response = self.client.post('/register/', data=self.form_data)
        self.assertContains(response, 'Password must contain at least one digit.', status_code=200)
        self.assertFalse(User.objects.filter(username="myuser").exists())
        self.assertEqual(User.objects.count(), 1)

    def test_dont_register_user_with_bad_password_case(self):
        self.form_data['password'] = 'mypassword1'
        self.form_data['password_confirm'] = 'mypassword1'
        response = self.client.post('/register/', data=self.form_data)
        self.assertContains(response, 'Password must contain at least one uppercase letter.', status_code=200)
        self.assertFalse(User.objects.filter(username="myuser").exists())
        self.assertEqual(User.objects.count(), 1)

class LoginFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

    def test_login_user_with_valid_form(self):
        response = self.client.post('/login/', data=self.form_data, follow=True)
        self.assertTemplateUsed(response, 'dashboard.html')
    
    def test_dont_login_user_with_invalid_credentials(self):
        self.form_data['password'] = 'myPassword1'
        response = self.client.post('/login/', data=self.form_data)
        self.assertContains(response, 'Incorrect username/password', status_code=200)
