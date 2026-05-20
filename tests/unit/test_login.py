"""Unit tests for the login functionality."""

import pytest

import server


class TestShowSummary:
    """Tests for the showSummary route (login via email)."""

    @pytest.fixture(autouse=True)
    def _mock_clubs(self, monkeypatch, mock_clubs):
        monkeypatch.setattr(server, "clubs", mock_clubs)

    def test_login_with_valid_email(self, client):
        """Test that a known email logs in successfully."""
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200
        assert b"Welcome" in response.data

    def test_login_with_unknown_email(self, client):
        """Test that an unknown email shows an error message instead of crashing."""
        response = client.post("/showSummary", data={"email": "unknown@test.com"})
        assert response.status_code == 200
        assert b"email was not found" in response.data

    def test_login_with_empty_email(self, client):
        """Test that an empty email shows an error message."""
        response = client.post("/showSummary", data={"email": ""})
        assert response.status_code == 200
        assert b"Sorry, that email was empty" in response.data

    def test_login_without_email_field(self, client):
        """Test that a missing email field shows an error message."""
        response = client.post("/showSummary", data={})
        assert response.status_code == 200
        assert b"Sorry, that email was empty" in response.data

    def test_login_with_whitespace_email(self, client):
        """Test that an email with surrounding whitespace is handled correctly."""
        response = client.post(
            "/showSummary", data={"email": "   john@simplylift.co   "}
        )
        assert response.status_code == 200
        assert b"Welcome" in response.data

    def test_login_with_uppercase_email(self, client):
        """Test that email matching is case-insensitive."""
        response = client.post("/showSummary", data={"email": "JOHN@SIMPLYLIFT.CO"})
        assert response.status_code == 200
        assert b"Welcome" in response.data
