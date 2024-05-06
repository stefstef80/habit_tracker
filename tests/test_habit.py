import datetime
import pytest
import json
from models.habit import Habit

# Test serialization to JSON
def test_to_json(predefined_habits):
    for habit in predefined_habits:
        habit_json = habit.to_json()
        habit_dict = json.loads(habit_json)  # Deserialize JSON to a Python dictionary for assertions
        assert habit_dict["name"] == habit.name
        assert habit_dict["periodicity"] == habit.periodicity.total_seconds()
        assert habit_dict["start_date"] == habit.start_date.isoformat()
        assert all(date == d for date, d in zip(habit_dict["completions"], [d.isoformat() for d in habit.completions]))

# Test deserialization from JSON
def test_from_json(predefined_habits):
    for habit in predefined_habits:
        habit_json = habit.to_json()
        habit_clone = Habit.from_json(habit_json)
        assert habit_clone.name == habit.name
        assert habit_clone.periodicity == habit.periodicity
        assert habit_clone.start_date == habit.start_date
        assert habit_clone.completions == habit.completions

# Test completing a habit
def test_complete(predefined_habits):
    for habit in predefined_habits:
        prev_count = len(habit.completions)
        habit.complete()
        assert len(habit.completions) == prev_count + 1
        assert habit.completions[-1] == datetime.date.today()

# Test current streak calculation
@pytest.mark.parametrize("index, expected_streak", [(0, 28), (1, 28), (2, 28), (3, 4), (4, 4)])
def test_current_streak(predefined_habits, index, expected_streak):
    habit = predefined_habits[index]
    assert habit.current_streak() == expected_streak

# Test habit with no completion dates
def test_habit_with_no_completion_dates():
    habit = Habit(name="Meditate", periodicity=datetime.timedelta(days=2))
    assert habit.current_streak() == 0
    habit_json = habit.to_json()
    assert json.loads(habit_json)["completions"] == []

    # Completing the habit and checking if it handles the first completion correctly
    habit.complete()
    assert habit.completions[-1] == datetime.date.today()
    assert len(habit.completions) == 1

# Test error handling in from_json method
@pytest.mark.parametrize("bad_json", [
    "{}",  # Empty dictionary
    json.dumps({"name": "Sleep", "periodicity": "wrong_type", "start_date": "2022-01-01", "completions": []}),  # Incorrect type
    json.dumps({"name": "Sleep", "periodicity": 86400, "start_date": "not_a_date", "completions": []})  # Bad date format
])
def test_from_json_errors(bad_json):
    with pytest.raises((KeyError, ValueError, TypeError)):
        Habit.from_json(bad_json)

# Test current streak with irregular completion dates
@pytest.mark.parametrize("completion_dates, expected_streak", [
    ([datetime.date.today() - datetime.timedelta(days=x) for x in reversed([0, 2, 4, 7, 11, 16])], 1),  # One-day streak
    ([datetime.date.today() - datetime.timedelta(days=x) for x in reversed([0, 1, 3, 6, 10, 15])], 2)   # Two-day streak
])
def test_irregular_streaks(completion_dates, expected_streak):
    habit = Habit(name="Write Journal", periodicity=datetime.timedelta(days=1), completion_dates=completion_dates)
    assert habit.current_streak() == expected_streak


# Test longest streak calculation
@pytest.mark.parametrize("index, expected_streak", [
    (0, 28),  # Daily habit, completed for 27 consecutive days
    (1, 28),  # Another daily habit, also completed for 27 consecutive days
    (2, 28),  # Yet another daily habit, completed for 27 consecutive days
    (3, 4),   # Weekly habit, completed for 3 weeks
    (4, 4)    # Another weekly habit, also completed for 3 weeks
])
def test_longest_streak(predefined_habits, index, expected_streak):
    habit = predefined_habits[index]
    assert habit.longest_streak() == expected_streak

