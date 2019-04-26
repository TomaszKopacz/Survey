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
    email = db.Column(db.String(20))
    name = db.Column(db.String(20))
    faculty = db.Column(db.String(20))
    is_drunk = db.Column(db.Integer)
    how_often_drunk = db.Column(db.Integer)
    planned_drunk = db.Column(db.Integer)

    def __init__(self, email, name, faculty, is_drunk, how_often_drunk, planned_drunk):
        self.email = email
        self.name = name
        self.faculty = faculty
        self.is_drunk = is_drunk
        self.how_often_drunk = how_often_drunk
        self.planned_drunk = planned_drunk


@app.route("/")
def welcome():
    return render_template('welcome_template.html')


@app.route("/survey/")
def show_form():
    return render_template('survey_template.html')


@app.route("/save", methods=['POST'])
def save():
    email = request.form["email"]
    name = request.form["name"]
    faculty = request.form["faculty"]
    is_drunk = request.form["is_drunk"]
    how_often_drunk = request.form["how_often_drunk"]
    planned_drunk = request.form["planned_drunk"]

    answer = Answer(email, name, faculty, is_drunk, how_often_drunk, planned_drunk)
    db.session.add(answer)
    db.session.commit()

    return redirect("/results/")


@app.route("/results/")
def show_results():
    answers = db.session.query(Answer).all()

    return render_template("results_template.html", data=answers)


if __name__ == "__main__":
    app.run(debug=True)

