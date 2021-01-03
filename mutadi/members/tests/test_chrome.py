"""Functional tests for members app"""
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

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestRegisterSelenium(LiveServerTestCase):
    """Selenium functional tests for user registration."""

    serialized_rollback = True

    def setUp(self):
        super().setUp()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.close()
        super().tearDown()

    def test_valid_live_register_page(self):
        """Register page should redirect to login page after sign up validation."""
        url = urllib.parse.urljoin(self.live_server_url, "/members/register/")
        self.driver.get(url)
        username = self.driver.find_element(By.ID, "id_username")
        first_name = self.driver.find_element(By.ID, "id_first_name")
        last_name = self.driver.find_element(By.ID, "id_last_name")
        email = self.driver.find_element(By.ID, "id_email")
        password1 = self.driver.find_element(By.ID, "id_password1")
        password2 = self.driver.find_element(By.ID, "id_password2")
        submit = self.driver.find_element(By.CLASS_NAME, "btn")
        time.sleep(5)
        self.driver.implicitly_wait(5)
        username.send_keys("BobRobert")
        first_name.send_keys("Bob")
        last_name.send_keys("Robert")
        email.send_keys("bobrobert@test.com")
        password1.send_keys("fglZfYmr%?,9")
        password2.send_keys("fglZfYmr%?,9")
        submit.click()

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (self.live_server_url, "/members/login")
        assert "Se connecter" in self.driver.page_source
        assert self.driver.page_source


class TestLoginSelenium(LiveServerTestCase):
    """Selenium functional tests for user login."""

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

    def tearDown(self):
        self.driver.close()
        super().tearDown()

    def test_valid_live_login_page(self):
        """Login page shoud redirect to home page after sign in validation."""
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s" % (self.live_server_url)
        assert "Accueil :: Mutadi" in self.driver.title


class TestChangePasswordSelenium(LiveServerTestCase):
    """Selenium functional tests for user chenge password process"""

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

    def tearDown(self):
        self.driver.close()
        super().tearDown()

    def test_valid_live_change_password_page(self):
        """Validate data entries on the change password page"""
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/members/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("m=9UaK^C,Tbq9N=T")
        new_password1.send_keys("%h2KtHFJ_%JY")
        new_password2.send_keys("%h2KtHFJ_%JY")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (
            self.live_server_url,
            "/members/change_password_success",
        )
        assert "Mot de passe modifié :: Mutadi" in self.driver.title
        assert (
            "Votre mot de passe a été modifié avec succès !"
            in self.driver.page_source
        )

    def test_invalid_live_change_password_with_personal_information(self):
        """Unvalidate data entries on the change password page with personal information"""
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/members/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("m=9UaK^C,Tbq9N=T")
        new_password1.send_keys(self.proto_user.username)
        new_password2.send_keys(self.proto_user.username)
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (
            self.live_server_url,
            "/members/password",
        )
        assert (
            "Le mot de passe est trop semblable "
            "au champ «&nbsp;nom d’utilisateur&nbsp;»."
        ) in self.driver.page_source

    def test_invalid_live_change_password_with_only_number(self):
        """Unvalidate data entries on the change password page with only number"""
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/members/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("m=9UaK^C,Tbq9N=T")
        new_password1.send_keys("12345678")
        new_password2.send_keys("12345678")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (
            self.live_server_url,
            "/members/password",
        )
        assert (
            "Ce mot de passe est entièrement numérique."
            in self.driver.page_source
        )

    def test_invalid_live_change_password_with_short_entries(self):
        """Unvalidate data entries on the change password page with short entries"""
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/members/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("m=9UaK^C,Tbq9N=T")
        new_password1.send_keys("Q=3")
        new_password2.send_keys("Q=3")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (
            self.live_server_url,
            "/members/password",
        )
        assert (
            "Ce mot de passe est trop court. "
            "Il doit contenir au minimum 8 caractères."
        ) in self.driver.page_source

    def test_invalid_live_change_password_with_differents_new_passwords(self):
        """Unvalidate data entries on the change password page with short entries"""
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/members/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("m=9UaK^C,Tbq9N=T")
        new_password1.send_keys("tbf:[D=5")
        new_password2.send_keys("kOx`Y{nM")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (
            self.live_server_url,
            "/members/password",
        )
        assert (
            "Les deux mots de passe ne correspondent pas."
            in self.driver.page_source
        )

    def test_invalid_live_change_password_with_wrong_old_password(self):
        """Unvalidate data entries on the change password page with short entries"""
        self.driver.get("%s%s" % (self.live_server_url, "/members/login/"))
        username = self.driver.find_element(By.ID, "id_username")
        password = self.driver.find_element(By.ID, "id_password")
        submit = self.driver.find_element(By.ID, "submit-button")
        username.send_keys(self.proto_user.username)
        password.send_keys("m=9UaK^C,Tbq9N=T")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        self.driver.get("%s%s" % (self.live_server_url, "/members/password/"))
        old_password = self.driver.find_element(By.ID, "id_old_password")
        new_password1 = self.driver.find_element(By.ID, "id_new_password1")
        new_password2 = self.driver.find_element(By.ID, "id_new_password2")
        submit = self.driver.find_element(By.ID, "submit-button")
        old_password.send_keys("m=9UaK^C,Tbq9123")
        new_password1.send_keys("kOx`Y{nM")
        new_password2.send_keys("kOx`Y{nM")
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        assert current_url == "%s%s" % (
            self.live_server_url,
            "/members/password",
        )
        assert (
            "Votre ancien mot de passe est incorrect. "
            "Veuillez le rectifier."
        ) in self.driver.page_source
