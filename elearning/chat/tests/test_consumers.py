from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class ChatViewsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='chatuser', password='pass')
        self.client.login(username='chatuser', password='pass')
        self.url = reverse('chat:chat-room', args=['global'])

    def test_chat_room_view_positive(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'global')

    def test_chat_room_view_unauthenticated_negative(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)