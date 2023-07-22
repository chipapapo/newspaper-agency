from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from faker import Faker
import random

from agency.models import Topic, Redactor, Newspaper


class TestSetUp(TestCase):
    fake = Faker()
    usernames = []

    def setUp(self) -> None:
        self.client = Client()

        self.topics_data = [
            {
                "name": self.fake.word()
            }
            for _ in range(50)
        ]
        Topic.objects.bulk_create(
            Topic(**topic)
            for topic in self.topics_data
        )
        self.topics = Topic.objects.all()

        self.redactors_data = [
            {
                "username": self.generate_unique_username(),
                "password": self.fake.password(),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "years_of_experience": self.fake.pyint(min_value=1, max_value=99),
            }
            for _ in range(150)
        ]
        get_user_model().objects.bulk_create(
            get_user_model()(**redactor)
            for redactor in self.redactors_data
        )
        self.redactors = Redactor.objects.all()

        self.newspapers_data = [
            {
                "title": self.fake.sentence(nb_words=6),
                "content": self.fake.paragraph(nb_sentences=3),
            }
            for _ in range(300)
        ]
        Newspaper.objects.bulk_create(
            Newspaper(**newspaper)
            for newspaper in self.newspapers_data
        )
        for newspaper in Newspaper.objects.all():
            newspaper.topic.add(
                *random.sample(
                    list(self.topics), random.randint(1, 5)
                )
            )
            newspaper.publishers.add(
                *random.sample(
                    list(self.redactors), random.randint(1, 5)
                )
            )
        self.newspapers = Newspaper.objects.all()

    def generate_unique_username(self):
        while True:
            username = self.fake.user_name()
            if not (username in self.usernames):
                self.usernames.append(username)
                return username
