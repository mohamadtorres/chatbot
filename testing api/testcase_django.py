from django.test import TestCase
from django.urls import reverse

class ChatbotAPITest(TestCase):
    def test_chatbot_endpoint(self):
        url = reverse('chatbot')  # Use the name from `urlpatterns`
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Chatbot Webside")