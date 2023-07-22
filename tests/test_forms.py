from django.urls import reverse

from tests.test_setup import TestSetUp


class PrivateTest(TestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.redactors[0])

    def test_search_topics(self):
        url = (
            reverse("agency:topic-list")
            + "?name="
            + self.topics_data[0]["name"][2:]
        )
        response = self.client.get(url)
        topics = [
            topic
            for topic in self.topics
            if topic.name[2:] == self.topics_data[0]["name"][2:]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            topics
        )

    def test_search_redactors(self):
        url = (
            reverse("agency:redactor-list")
            + "?username="
            + self.redactors_data[0]["username"][2:]
        )
        response = self.client.get(url)
        redactors = [
            redactor
            for redactor in self.redactors
            if redactor.username[2:] == self.redactors_data[0]["username"][2:]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["redactor_list"]), redactors)

    def test_search_newspapers(self):
        url = (
                reverse("agency:newspaper-list")
                + "?title="
                + self.newspapers_data[0]["title"][2:]
        )
        response = self.client.get(url)
        newspapers = [
            newspaper
            for newspaper in self.newspapers
            if newspaper.title[2:] == self.newspapers_data[0]["title"][2:]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["newspaper_list"]), newspapers)

    def test_redactor_clean(self):
        data_clean = {
            "username": "test.user",
            "email": "test@email.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "Password123!@#",
            "password2": "Password123!@#",
            "years_of_experience": "5"
        }
        data_unclean = {
            "username": "test.user",
            "email": "test@email.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "Password123!@#",
            "password2": "Password123!@#",
            "years_of_experience": "105"
        }

        response_clean = self.client.post(
            reverse("agency:redactor-create"),
            data_clean
        )
        response_unclean = self.client.post(
            reverse("agency:redactor-create"),
            data_unclean
        )

        self.assertEqual(response_clean.status_code, 302)
        self.assertEqual(response_unclean.status_code, 200)
