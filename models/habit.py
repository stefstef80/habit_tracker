import json
from datetime import date, timedelta,datetime

class Habit:
    """
    Represents a habit with details such as its name, periodicity, start date, and completions.
    Attributes:
        name (str): The name of the habit.
        periodicity (timedelta): How often the habit should be completed.
        start_date (date): The start date of the habit.
        completions (list[date]): Dates when the habit was completed.
    """
    def __init__(self, name, periodicity, completion_dates=None, last_completed=None):
        """
        Initializes a new habit with a name and periodicity.
        Args:
            name (str): Name of the habit.
            periodicity (timedelta): Periodicity of the habit.
        """
        self.name = name
        self.periodicity = periodicity
        self.start_date = date.today()
        self.completions = completion_dates if completion_dates else []
        self.last_completed = last_completed or datetime.now()

    def complete(self, completion_date=None):
        """
        Marks the habit as completed on a specific date.
        Args:
            completion_date (date, optional): The date on which the habit was completed. Defaults to today.
        """
        if not completion_date:
            completion_date = date.today()
        self.completions.append(completion_date)

    def to_json(self):
        """
        Serializes the habit to a JSON-compatible dictionary.
        Returns:
            str: A JSON string of the habit's data.
        """
        return json.dumps({
            'name': self.name,
            'periodicity': self.periodicity.total_seconds(),
            'start_date': self.start_date.isoformat(),
            'completions': [d.isoformat() for d in self.completions]
        })

    @classmethod
    def from_json(cls, data):
        """
        Deserializes a Habit instance from a JSON string.
        Args:
            data (str): JSON string containing the habit's data.
        Returns:
            Habit: An instance of Habit.
        """
        data = json.loads(data)
        instance = cls(data['name'], timedelta(seconds=int(data['periodicity'])))
        instance.start_date = date.fromisoformat(data['start_date'])
        instance.completions = [date.fromisoformat(d) for d in data['completions']]
        return instance

    def current_streak(self):
        """
        Calculates the number of consecutive periods the habit has been completed without a break.
        Returns:
            int: The current streak of consecutive periods.
        """
        if not self.completions:
            return 0
        sorted_completions = sorted(self.completions)
        streak = 1
        for i in range(len(sorted_completions) - 1, 0, -1):
            if (sorted_completions[i] - sorted_completions[i - 1]).days <= self.periodicity.days:
                streak += 1
            else:
                break
        return streak

    def longest_streak(self):
        if not self.completions:
            return 0
        sorted_completions = sorted(self.completions)
        max_streak = 1
        current_streak = 1
        # Consider the periodicity in the day gap calculation
        for i in range(1, len(sorted_completions)):
            # Check if the gap between current and previous completion matches the periodicity
            if (sorted_completions[i] - sorted_completions[i - 1]).days == self.periodicity.days:
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1
        return max(max_streak, current_streak)
