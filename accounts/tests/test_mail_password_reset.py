from django.core import mail
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase



class PasswordResetMailTests(TestCase):
    test_email = 'ruslan.rybak@gmail.com'
    def setUp(self):
        UserModel = get_user_model()
        UserModel.objects.create_user(first_name='John', last_name='Doe', email=self.test_email, password='abcefg123')
        self.response = self.client.post(reverse('password_reset'), { 'email': self.test_email })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Lobsterlobby.com] Passwort zurücksetzen', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        # self.assertIn('john', self.email.body)
        self.assertIn(self.test_email, self.email.body)

    def test_email_to(self):
        self.assertEqual([self.test_email,], self.email.to)
