import datetime
import pytest


# Habit fixtures for testing
from models.habit import Habit

@pytest.fixture(scope="module")
def predefined_habits():
    now = datetime.date.today()  # Use date.today() for date comparisons and manipulations
    return [
        Habit(
            name="Read Book",
            periodicity=datetime.timedelta(days=1),
            completion_dates=[now - datetime.timedelta(days=x) for x in range(1, 28)],
            last_completed=now - datetime.timedelta(days=1)
        ),
        Habit(
            name="Drink Water",
            periodicity=datetime.timedelta(days=1),
            completion_dates=[now - datetime.timedelta(days=x) for x in range(1, 28)],
            last_completed=now - datetime.timedelta(days=1)
        ),
        Habit(
            name="Practice Guitar",
            periodicity=datetime.timedelta(days=1),
            completion_dates=[now - datetime.timedelta(days=x) for x in range(1, 28)],
            last_completed=now - datetime.timedelta(days=1)
        ),
        Habit(
            name="Jogging",
            periodicity=datetime.timedelta(days=7),
            completion_dates=[now - datetime.timedelta(days=7 * x) for x in range(1, 4)],
            last_completed=now - datetime.timedelta(days=7)
        ),
        Habit(
            name="Weekly Review",
            periodicity=datetime.timedelta(days=7),
            completion_dates=[now - datetime.timedelta(days=7 * x) for x in range(1, 4)],
            last_completed=now - datetime.timedelta(days=7)
        )
    ]

