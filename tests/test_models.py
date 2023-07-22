from django.urls import reverse

from tests.test_setup import TestSetUp


class ModelTests(TestSetUp):
    def test_topic_str(self):
        self.topic = self.topics[0]

        self.assertEqual(
            str(self.topic),
            self.topic.name
        )

    def test_redactor_str(self):
        self.redactor = self.redactors[0]

        self.assertEqual(
            str(self.redactor),
            f"{self.redactor.first_name} {self.redactor.last_name} "
            f"({self.redactor.username})"
        )

    def test_newspaper_str(self):
        self.newspaper = self.newspapers[0]

        self.assertEqual(
            str(self.newspaper),
            f"{self.newspaper.title} ({self.newspaper.published_date})"
        )
