"""Shared test fixtures for the GUDLFT application."""

import pytest
from server import app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_clubs():
    """Return sample club data for testing."""
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]


@pytest.fixture
def mock_competitions():
    """Return sample competition data for testing."""
    return [
        {
            "name": "Spring Festival",
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": "2026-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
    ]
