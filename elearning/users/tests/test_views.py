from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class UserViewsTest(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student', password='pass123', role='Student'
        )
        self.profile_url = reverse('users:profile')

    def test_profile_view_positive(self):
        """Positive: logged-in student can view their profile."""
        self.client.login(username='student', password='pass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'student')

    def test_profile_view_unauthenticated_negative(self):
        """Negative: unauthenticated user cannot access profile."""
        response = self.client.get(self.profile_url)
        self.assertNotEqual(response.status_code, 200)  # Possibly 302 or 403