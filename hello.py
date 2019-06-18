from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://asiopgjackioyq' \
                                        ':77c694ab09e3fcf8c89a8ca55056c19ebc4be7d6ab4e8b27854670c123948bf1@ec2-54-225' \
                                        '-242-183.compute-1.amazonaws.com:5432/d6i8f80sqi62dd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)


class Answer(db.Model):
    __table_name__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    age = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    living = db.Column(db.String(10))
    earnings = db.Column(db.String(50))

    season = db.Column(db.String(10))
    place = db.Column(db.String(10))
    favourite = db.Column(db.String(50))
    accommodation = db.Column(db.String(20))
    mean = db.Column(db.String(15))
    planning = db.Column(db.String(50))
    partners = db.Column(db.String(50))
    is_active = db.Column(db.String(50))
    activity = db.Column(db.String(50))
    last_holidays = db.Column(db.String(50))
    abroad = db.Column(db.String(50))
    arrangements = db.Column(db.String(100))
    expenses = db.Column(db.String(30))

    def __init__(self,
                 age,
                 sex,
                 living,
                 earnings,
                 season,
                 place,
                 favourite,
                 accommodation,
                 mean,
                 planning,
                 partners,
                 is_active,
                 activity,
                 last_holidays,
                 abroad,
                 arrangements,
                 expenses):
        self.age = age
        self.sex = sex
        self.living = living
        self.earnings = earnings
        self.season = season
        self.place = place
        self.favourite = favourite
        self.accommodation = accommodation
        self.mean = mean
        self.planning = planning
        self.partners = partners
        self.is_active = is_active
        self.activity = activity
        self.last_holidays = last_holidays
        self.abroad = abroad
        self.arrangements = arrangements
        self.expenses = expenses


@app.route("/")
def welcome():
    return render_template('welcome_template.html')


@app.route("/survey/")
def show_form():
    return render_template('survey_template.html')


@app.route("/save", methods=['POST'])
def save():
    _age = request.form["age"]
    _sex = request.form["sex"]
    _living = request.form["living"]
    _earnings = request.form["earnings"]

    _season = request.form["season"]
    _place = request.form["place"]
    _favourite = request.form["favourite"]
    _favourite_text = request.form["favourite_text"]
    _accommodation = request.form["accommodation"]
    _mean = request.form["mean"]
    _planning = request.form["planning"]
    _partners = request.form["partners"]
    _partners_text = request.form["partners_text"]
    _is_active = request.form["is_active"]
    _activity = request.form["activity"]
    _last_holidays = request.form["last_holidays"]
    _abroad = request.form["abroad"]
    _arrangements = request.form["arrangements"]
    _expenses = request.form["expenses"]

    answer = Answer(_age,
                    _sex,
                    _living,
                    _earnings,
                    _season,
                    _place,
                    get_favourite(_favourite, _favourite_text),
                    _accommodation,
                    _mean,
                    _planning,
                    get_partners(_partners, _partners_text),
                    _is_active,
                    _activity,
                    _last_holidays,
                    _abroad,
                    _arrangements,
                    _expenses)
    db.session.add(answer)
    db.session.commit()

    return redirect("/results/")


def get_favourite(_favourite, _favourite_text):
    if _favourite == "Tak":
        return _favourite_text

    else:
        return _favourite


def get_partners(_partners, _partners_text):
    if _partners == "Inne":
        return _partners_text

    else:
        return _partners


@app.route("/results/")
def show_results():
    answers = db.session.query(Answer).all()

    return render_template("results_template.html", data=answers)


@app.route("/info/")
def info():
    return render_template('info_template.html')


if __name__ == "__main__":
    app.run(debug=True)

