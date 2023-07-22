from django.urls import reverse

from tests.test_setup import TestSetUp
from agency.models import Redactor

TOPIC_LIST_URL = reverse("agency:topic-list")
REDACTOR_LIST_URL = reverse("agency:redactor-list")
NEWSPAPER_LIST_URL = reverse("agency:newspaper-list")



class PublicTests(TestSetUp):
    def test_login_required_topic_list(self):
        response = self.client.get(TOPIC_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_redactor_list(self):
        response = self.client.get(REDACTOR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_redactor_detail(self):
        response = self.client.get(
            reverse("agency:redactor-detail", kwargs={"pk": self.redactors[0].pk})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_newspaper_list(self):
        response = self.client.get(NEWSPAPER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_newspaper_detail(self):
        response = self.client.get(
            reverse("agency:newspaper-detail", kwargs={"pk": self.newspapers[0].pk})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_register(self):
        data = {
            "username": "test.user",
            "email": "test@email.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "Password123!@#",
            "password2": "Password123!@#",
            "years_of_experience": "5"
        }
        response_get = self.client.get(
            reverse("register")
        )
        response_post = self.client.post(
            reverse("register"), data
        )

        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_post.status_code, 302)

        self.assertTrue(Redactor.objects.filter(username=data["username"]))
        self.assertTrue(Redactor.objects.filter(email=data["email"]))



class PrivateTests(TestSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.redactors[0])

    def test_retrieve_topics(self):
        response = self.client.get(TOPIC_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"][:10]),
            list(self.topics[:10])
        )
        self.assertTemplateUsed(response, "agency/topic_list.html")

    def test_retrieve_drivers(self):
        response = self.client.get(REDACTOR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["redactor_list"][:10]),
            list(self.redactors[:10])
        )
        self.assertTemplateUsed(response, "agency/redactor_list.html")

    def test_retrieve_cars(self):
        response = self.client.get(NEWSPAPER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["newspaper_list"])[:10],
            list(self.newspapers)[:10]
        )
        self.assertTemplateUsed(response, "agency/newspaper_list.html")

    def test_toggle_newspaper(self):
        self.client.post(
            reverse(
                "agency:toggle-newspaper-assign",
                kwargs={"pk": self.newspapers[0].pk}
                    )
        )

        self.assertEqual(
            list(self.redactors[0].redactors.all())[-1],
            self.newspapers[0]
        )

    def test_logout(self):
        response = self.client.get(
            reverse("logout")
        )

        self.assertEqual(response.status_code, 200)
