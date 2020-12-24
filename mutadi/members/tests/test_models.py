"""Unit tests for memebers app models"""
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from mutadi.members.models import Profile

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestProfileModel:
    """Group multiple tests in Category model"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_using_profile(self, proto_user):
        """Function should be using fixture of profile baked model."""
        assert isinstance(proto_user.profile, Profile)

    def test___str__profile_model(self, proto_user):
        """__str__() method should be the profile title."""
        assert proto_user.profile.__str__() == str(proto_user.profile)
        assert str(proto_user.profile) == str(proto_user.profile)

    def test_get_absolute_url(self, proto_user):
        """get_absolute_url() should be reirected to home page."""
        assert proto_user.profile.get_absolute_url() == "/"

    def test_verbose_name_plural_profiles(self, proto_user):
        """verbose_name_plural should be categories."""
        assert proto_user.profile._meta.verbose_name_plural == "profiles"

    def test_profile_picture_label(self, proto_user):
        """Title label profile picture should be profile_pic."""
        field_label = proto_user.profile._meta.get_field(
            "profile_pic"
        ).verbose_name
        assert field_label == "profile pic"

    def test_profile_pic_default(self, proto_user):
        """Default for profile picture field should be True."""
        default = proto_user.profile._meta.get_field("profile_pic").default
        assert default

    def test_profile_pic_upload_to(self, proto_user):
        """Upload_to for profile picture field should be True."""
        upload_to = proto_user.profile._meta.get_field("profile_pic").upload_to
        assert upload_to

    def test_profile_exists(self, proto_user):
        """Profile should exists with baked Profile model."""
        assert Profile.objects.count() == 1
