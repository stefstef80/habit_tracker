import datetime
import json
import pytest
from unittest.mock import patch, MagicMock
from models.habit import Habit
from models.habit_tracker import HabitTracker

import datetime
import json
import pytest
from unittest.mock import patch, mock_open
from models.habit import Habit
from models.habit_tracker import HabitTracker
from datetime import timedelta

import datetime
import json
import pytest
from unittest.mock import patch, mock_open
from models.habit import Habit
from models.habit_tracker import HabitTracker




@pytest.fixture
def habit_tracker():
    # Prepare some sample data as it would be stored in a file

    now = datetime.date.today()
    habits_data = {
        "Read Book":{
            "name": "Read Book",
            "periodicity": timedelta(days=1).total_seconds(),
            "start_date": "2023-01-01",
            "completions": ["2023-01-02", "2023-01-03"]
        },
        "Drink Water":{
            "name": "Drink Water",
            "periodicity": timedelta(days=1).total_seconds(),
            "start_date": (now - datetime.timedelta(days=28)).isoformat(),
            "completions": [(now - datetime.timedelta(days=x)).isoformat() for x in range(1, 29)]
        },
        "Practice Guitar":{
            "name": "Practice Guitar",
            "periodicity": timedelta(days=1).total_seconds(),
            "start_date": (now - datetime.timedelta(days=28)).isoformat(),
            "completions": [(now - datetime.timedelta(days=x)).isoformat() for x in range(1, 28)]
        },
        "Jogging":{
            "name": "Jogging",
            "periodicity": timedelta(days=7).total_seconds(),
            "start_date": (now - datetime.timedelta(days=28)).isoformat(),
            "completions": [(now - datetime.timedelta(days=7 * x)).isoformat() for x in range(1, 4)]
        },
        "Weekly Review":{
            "name": "Weekly Review",
            "periodicity": timedelta(days=7).total_seconds(),
            "start_date": (now - datetime.timedelta(days=28)).isoformat(),
            "completions": [(now - datetime.timedelta(days=7 * x)).isoformat() for x in range(1, 4)]
        }
    }

    habits_json = json.dumps(habits_data)
    with patch('builtins.open', mock_open(read_data=habits_json)), patch('os.path.exists', return_value=True):
        tracker = HabitTracker()
        return tracker

def test_load_habits(habit_tracker):
    # Assuming the HabitTracker loads habits in its constructor or a method call
    assert len(habit_tracker.habits) == 5
    assert habit_tracker.habits["Read Book"].name == "Read Book"

def test_complete_habit(habit_tracker):
    habit_name = "Read Book"
    original_completions = len(habit_tracker.habits[habit_name].completions)
    habit_tracker.complete_habit(habit_name)
    assert len(habit_tracker.habits[habit_name].completions) == original_completions + 1

def test_daily_habits(habit_tracker):
    daily_habits = habit_tracker.daily_habits()
    assert sorted(daily_habits) == sorted(["Read Book", "Drink Water","Practice Guitar"])

def test_most_struggled_habits_last_month(habit_tracker):
    struggled_habits = habit_tracker.most_struggled_habits_last_month()
    assert 'Read Book' in struggled_habits

def test_habits_with_periodicity(habit_tracker):
    daily_habits = habit_tracker.habits_with_periodicity(timedelta(days=1))
    assert sorted(daily_habits) == ["Drink Water", "Practice Guitar", "Read Book"]
    weekly_habits = habit_tracker.habits_with_periodicity(timedelta(days=7))
    assert sorted(weekly_habits) == ["Jogging", "Weekly Review"]

def test_longest_streak_of_all_habits(habit_tracker):
    assert habit_tracker.longest_streak_of_all_habits() == 28  # Assuming "Drink Water" has the longest streak

def test_longest_streak(habit_tracker):
    assert habit_tracker.longest_streak("Drink Water") == 28
    assert habit_tracker.longest_streak("Jogging") == 3
    assert habit_tracker.longest_streak("Nonexistent Habit") == 0  # Testing for a habit that does not exist


