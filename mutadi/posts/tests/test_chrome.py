"""Functional tests for users app
"""
import time
import urllib.parse

import pytest
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from model_bakery import baker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from mutadi.posts.models import Post

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestChangePasswordSelenium(LiveServerTestCase):
    serialized_rollback = True

    def setUp(self):
        super().setUp()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options=options)
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        self.proto_post = baker.make(
            Post, content="This is a Post", author=self.proto_user
        )

    def tearDown(self):
        self.driver.close()
        super().tearDown()

    def test_valid_live_delete_post_page(self):
        """
        After confirmation of the deletion of a post,
        it should send a message of success on home page
        """
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get(
            "%s%s"
            % (
                self.live_server_url,
                f"/posts/post_detail/{self.proto_post.pk}/remove",
            )
        )
        delete = self.driver.find_element(By.ID, "id_delete_post")
        delete.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s" % (self.live_server_url,)
        assert (
            "La publication a été supprimée avec succès !"
            in self.driver.page_source
        )