# Habit Tracker Application

## Overview
This Python-based Habit Tracker helps users track and maintain their daily habits. It utilizes Flask to serve web content and manages habit data using a simple JSON file, ensuring ease of use and setup.

## Installation
bash
pip install flask
Prerequisites
Python 3.6 or higher
Flask
An environment to run Flask applications
Setup
Clone the repository:
git clone https://github.com/stefstef80/habit_tracker.git



# Core Classes and Methods
The two main (and only) classes are the Habit and HabitTracker classes.

##Habit Class
The Habit class represents an individual habit. It encapsulates all the properties and methods necessary for managing a habit's lifecycle, such as tracking completions and calculating streaks.

### Properties
name (str): The name of the habit.
periodicity (timedelta): The frequency with which the habit should be completed.
start_date (date): The date when the habit tracking started.
completions (list[date]): A list of dates when the habit was completed.

### Methods
complete(completion_date=date.today()): Marks the habit as completed on a given date. If no date is provided, it defaults to today's date.
to_json(): Serializes the habit to a JSON-compatible dictionary for storage.
from_json(data): Deserializes a JSON string into a Habit instance.
current_streak(): Calculates the current streak of consecutive completions based on the periodicity.
longest_streak(): Determines the longest streak of consecutive completions.



## HabitTracker Class
The HabitTracker class manages a collection of Habit instances. It provides functionality to add habits, track completions, and retrieve habit-related statistics.

### Properties
file_path (str): The path to the JSON file where habits are stored.

### Methods
add_habit(habit): Adds a new Habit instance to the tracker.
load_habits(): Loads all habits from the JSON file.
save_habits(): Saves all habits to the JSON file.
complete_habit(habit_name, date=date.today()): Marks a specified habit as completed on a given date.
daily_habits(): Returns a list of habits with a daily periodicity.
most_struggled_habits_last_month(): Identifies habits with the fewest completions in the last month.
habits_with_periodicity(periodicity): Returns a list of all habits with the specified periodicity.
longest_streak_of_all_habits(): Returns the longest streak across all habits.
longest_streak(habit_name): Returns the longest streak for a specific habit.



Usage

once you cloned the project and installed flaks, run the command (in your terminal):
python -m flask run

Visit http://localhost:5000 in your web browser to access the Habit Tracker.
