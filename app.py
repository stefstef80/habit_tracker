from flask import Flask, request, render_template, redirect, url_for
import json
import os
from datetime import date, timedelta

from models.habit import Habit
from models.habit_tracker import HabitTracker

app = Flask(__name__)
tracker = HabitTracker('habits.json')

@app.route('/')
def index():
    return render_template('index.html',
                           habits=tracker.habits.values(),
                           longest_streak_all=tracker.longest_streak_of_all_habits(),
                           daily_habits=tracker.daily_habits(),
                           struggled_last_month=tracker.most_struggled_habits_last_month(),
                           periodicity_habits=None)

@app.route('/habits_by_periodicity', methods=['GET', 'POST'])
def habits_by_periodicity():
    if request.method == 'POST':
        periodicity_days = int(request.form['periodicity_days'])
        periodicity_habits = tracker.habits_with_periodicity(timedelta(days=periodicity_days))
        return render_template('index.html',
                               habits=tracker.habits.values(),
                               longest_streak_all=tracker.longest_streak_of_all_habits(),
                               daily_habits=tracker.daily_habits(),
                               struggled_last_month=tracker.most_struggled_habits_last_month(),
                               periodicity_habits=periodicity_habits)
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form['name']
        periodicity_days = int(request.form['periodicity_days'])
        periodicity = timedelta(days=periodicity_days)
        habit = Habit(name, periodicity)
        tracker.add_habit(habit)
        return redirect(url_for('index'))
    return render_template('add_habit.html')

@app.route('/complete/<habit_name>')
def complete_habit(habit_name):
    tracker.complete_habit(habit_name, date.today())
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
