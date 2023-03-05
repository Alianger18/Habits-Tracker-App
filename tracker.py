import datetime

class Tracker:

    # Setting the count of habits created
    count = 5

    def __init__(self, name, periodicity):
        """
        Create habits based on simple parameters in order to create class objects and store them
        in a separate list with a unified order, a count variable is also incremented everytime
        a habit has been created.
        :param name: The name of the habit
        :param periodicity: The frequency of this habit
        """

        # Updating the count
        Tracker.count += 1

        # Setting the attributes
        self.habit_id = self.count
        self.name = name
        self.periodicity = periodicity
        self.start_date = datetime.date.today()
        self.streak_ongoing = 0

        # This attribute hold every detail related to a given habit
        self.details = [self.habit_id, self.name, self.periodicity, self.streak_ongoing]
