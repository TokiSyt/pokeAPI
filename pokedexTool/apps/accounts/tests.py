import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestCustomUserModel:
    @pytest.mark.django_db
    def test_create_user(self, user_factory):
        user = user_factory(username="testuser")
        assert user.username == "testuser"
        assert user.check_password("testpass123")

    @pytest.mark.django_db
    def test_str_returns_username(self, user):
        assert str(user) == user.username

    @pytest.mark.django_db
    def test_create_superuser(self, admin_user):
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True


class TestSignUpView:
    @pytest.mark.django_db
    def test_signup_page_renders(self, client):
        response = client.get(reverse("accounts:signup"))
        assert response.status_code == 200
        assert b"Create" in response.content or b"account" in response.content.lower()

    @pytest.mark.django_db
    def test_signup_creates_user(self, client):
        response = client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "password1": "complexpass123!",
                "password2": "complexpass123!",
            },
        )
        assert response.status_code == 302  # redirect on success
        assert User.objects.filter(username="newuser").exists()

    @pytest.mark.django_db
    def test_signup_password_mismatch(self, client):
        response = client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "password1": "complexpass123!",
                "password2": "differentpass!",
            },
        )
        assert response.status_code == 200  # stays on page
        assert not User.objects.filter(username="newuser").exists()


class TestLoginLogout:
    @pytest.mark.django_db
    def test_login_page_renders(self, client):
        response = client.get(reverse("login"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_login_valid_credentials(self, client, user):
        response = client.post(
            reverse("login"),
            {"username": user.username, "password": "testpass123"},
        )
        assert response.status_code == 302  # redirect on success

    @pytest.mark.django_db
    def test_login_invalid_credentials(self, client, user):
        response = client.post(
            reverse("login"),
            {"username": user.username, "password": "wrongpassword"},
        )
        assert response.status_code == 200  # stays on login page

    @pytest.mark.django_db
    def test_logout(self, client, user):
        client.force_login(user)
        response = client.post(reverse("logout"))
        assert response.status_code == 302  # redirect after logout
