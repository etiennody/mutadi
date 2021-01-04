"""Functional tests for private_messages app"""
import time

import pytest
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from model_bakery import baker
from mutadi.private_messages.models import PrivateMessage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestDeleteMessagesSelenium(LiveServerTestCase):
    """Selenium functional tests for deletion of post."""

    serialized_rollback = True

    def setUp(self):
        super().setUp()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options=options)
        self.proto_user_a = baker.make(User)
        self.proto_user_a.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user_a.save()
        self.proto_user_b = baker.make(User)
        self.proto_user_b.set_password("3$0aF/gxFsinR'6k")
        self.proto_user_b.save()
        self.proto_private_message = baker.make(
            PrivateMessage,
            sender=self.proto_user_a,
            recipient=self.proto_user_b,
            content=(
                "Proident nisi cillum sit tempor "
                "reprehenderit proident in non fugiat ex id."
            ),
        )

    def tearDown(self):
        self.driver.close()
        super().tearDown()

    def test_valid_live_delete_message_page(self):
        """
        After confirmation of the deletion of a message,
        it should send a message of success on inbox.
        """
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user_b.username)
        password.send_keys("3$0aF/gxFsinR'6k")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/messages/inbox/"))
        delete = self.driver.find_element(By.ID, "id_delete_message")
        delete.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (
            self.live_server_url,
            f"/messages/message_detail/{self.proto_private_message.pk}/delete",
        )
        assert "Message supprimé avec succès !" in self.driver.page_source
