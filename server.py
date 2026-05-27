import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for

from helpers import find_club_by_email, find_competition, find_club


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.context_processor
def inject_now():
    """Expose the current datetime as a string to all templates."""
    return {"now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """Log in a club secretary by email and show the welcome page."""
    email = request.form.get("email", "").strip()

    if not email:
        flash("Sorry, that email was empty. Please try again.")
        return render_template("index.html")

    club = find_club_by_email(clubs, email)

    if club is None:
        flash("Sorry, that email was not found. Please try again.")
        return render_template("index.html")

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Display the booking form for a given competition and club."""
    foundClub = find_club(clubs, club)
    foundCompetition = find_competition(competitions, competition)

    if foundClub is None or foundCompetition is None:
        flash("Something went wrong. Please try again")
        return redirect(url_for("index"))

    competition_date = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("This competition has already taken place. You cannot book places.")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )
    return render_template("booking.html", club=foundClub, competition=foundCompetition)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """Purchase places for a competition using club points."""
    competition = find_competition(competitions, request.form["competition"])
    club = find_club(clubs, request.form["club"])

    if competition is None or club is None:
        flash("Something went wrong. Please try again")
        return redirect(url_for("index"))

    placesRequired = int(request.form["places"])

    if placesRequired > 12:
        flash("Cannot book more than 12 places per competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if placesRequired > int(club["points"]):
        flash("Not enough points available.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if placesRequired > int(competition["numberOfPlaces"]):
        flash("Not enough places available in this competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    club["points"] = str(int(club["points"]) - placesRequired)
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
