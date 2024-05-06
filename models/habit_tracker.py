from collections import defaultdict


import datetime
import json
from firebase_admin import firestore

from models.habit import Habit

import json
import os
from datetime import datetime


import json
import os
from datetime import date, timedelta, datetime
from flask import Flask, request, render_template, redirect, url_for

class HabitTracker:
    """
    Manages a collection of habits and handles their storage and retrieval.
    """
    def __init__(self, file_path='habits.json'):
        """
        Initializes the HabitTracker with a path to a JSON file.
        Args:
            file_path (str): Path to the JSON file where habits are stored.
        """
        self.file_path = file_path
        self.habits = {}
        self.load_habits()

    def add_habit(self, habit):
        """
        Adds a new habit to the tracker and saves it.
        Args:
            habit (Habit): The habit to add.
        """
        self.habits[habit.name] = habit
        self.save_habits()

    def load_habits(self):
        """
        Loads all habits from the JSON file.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                for name, habit_data in data.items():
                    self.habits[name] = Habit.from_json(json.dumps(habit_data))

    def save_habits(self):
        """
        Saves all habits to the JSON file.
        """
        with open(self.file_path, 'w') as file:
            json.dump({name: json.loads(habit.to_json()) for name, habit in self.habits.items()}, file)
            # json.dump({"test": "data"}, file)

    def complete_habit(self, habit_name, date=None):
        """
        Marks a specified habit as completed on a given date.
        Args:
            habit_name (str): Name of the habit to complete.
            date (date, optional): Date of completion. Defaults to today.
        """
        if habit_name in self.habits:
            self.habits[habit_name].complete(date)
            self.save_habits()

    def daily_habits(self):
        """
        Return a list of habits that have a daily periodicity.
        Returns:
            list[str]: Names of daily habits.
        """
        return [name for name, habit in self.habits.items() if habit.periodicity == timedelta(days=1)]

    def most_struggled_habits_last_month(self):
        """
        Identify habits with the fewest completions in the last month.
        Returns:
            list[str]: Names of the habits that were least completed last month.
        """
        last_month = date.today() - timedelta(days=30)
        habits_last_month = {
            name: len([completion_date for completion_date in habit.completions if completion_date >= last_month])
            for name, habit in self.habits.items()
        }
        min_completions = min(habits_last_month.values(), default=float('inf'))
        return [name for name, count in habits_last_month.items() if count == min_completions]

    def habits_with_periodicity(self, periodicity):
        """
        Return a list of all habits with the specified periodicity.
        Args:
            periodicity (timedelta): Periodicity to search for.
        Returns:
            list[str]: Names of habits with the specified periodicity.
        """
        return [name for name, habit in self.habits.items() if habit.periodicity == periodicity]

    def longest_streak_of_all_habits(self):
        """
        Return the longest streak across all habits.
        Returns:
            int: The longest streak of any habit.
        """
        return max((habit.current_streak() for habit in self.habits.values()), default=0)

    def longest_streak(self, habit_name):
        """
        Return the longest streak for a specific habit.
        Args:
            habit_name (str): Name of the habit to check.
        Returns:
            int: The longest streak of habit completion.
        """
        if habit_name in self.habits:
            return self.habits[habit_name].current_streak()
        return 0


