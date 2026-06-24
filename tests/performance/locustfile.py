"""Locust load-test scenarios for the GUDLFT application."""

import random

from locust import HttpUser, between, task

CLUB_EMAILS = [
    "john@simplylift.co",
    "admin@irontemple.com",
    "kate@shelifts.co.uk",
]


class GUDLFTUser(HttpUser):
    """A simulated club secretary navigating the app."""

    wait_time = between(1, 3)

    @task(3)
    def view_points_board(self):
        """The public points board: read-only, lightest endpoint."""
        self.client.get("/points-board")

    @task(2)
    def login_and_view_welcome(self):
        """Log in with a random known email and stay on the welcome page."""
        email = random.choice(CLUB_EMAILS)
        self.client.post("/showSummary", data={"email": email}, name="/showSummary")

    @task(1)
    def book_one_place_on_future_competition(self):
        """End-to-end: log in, open the booking page, buy one place."""
        self.client.post(
            "/showSummary", data={"email": "john@simplylift.co"}, name="/showSummary"
        )
        self.client.get(
            "/book/Fall%20Classic/Simply%20Lift", name="/book/[competition]/[club]"
        )
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Simply Lift",
                "places": "1",
            },
            name="/purchasePlaces",
        )
