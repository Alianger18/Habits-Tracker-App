from tracker import Tracker
import pandas as pd
import datetime
import sqlite3

def get_db(name="main.db"):
    """
    Create our database.
    :param name: The name of a database file.
    :return: A connection to our database.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    """
    This method creates 2 tables to store data.
    HABITS_STREAK_ONGOING : Holds information about the ongoing habits.
    HABITS_STREAK_HISTORY : Holds information about the habits formerly broken.
    :param db: a database.
    :return: None.
    """
    # Creating a cursor object
    cur = db.cursor()

    # Creating tables
    # ONGOING_HABITS is a table tracking current tables
    cur.execute(
        "CREATE TABLE IF NOT EXISTS ACTIVE_HABITS ("
        "HABIT_ID SMALLINT PRIMARY KEY UNIQUE,"
        "HABIT_NAME VARCHAR,"
        "PERIODICITY VARCHAR,"
        "LAST_INCREMENTATION_DATE DATE,"
        "STREAK_ONGOING SMALLINT"
        ")"
    )

    # TRACKING_HABITS is a table tracking creating, breaking, deleting, resetting, and incrementing habits
    cur.execute(
        "CREATE TABLE IF NOT EXISTS TRACKING_HABITS ("
        "EVENT_TIMESTAMP VARCHAR PRIMARY KEY UNIQUE, "
        "HABIT_ID SMALLINT, "
        "EVENT_NAME VARCHAR"
        ")"
    )

    # BROKEN_HABITS is a table tracking broken habits
    cur.execute(
        "CREATE TABLE IF NOT EXISTS BROKEN_HABITS ("
        "HABIT_ID SMALLINT PRIMARY KEY UNIQUE,"
        "HABIT_NAME VARCHAR,"
        "PERIODICITY VARCHAR,"
        "START_DATE DATE,"
        "END_DATE DATE,"
        "STREAK_ENDED SMALLINT"
        ")"
    )

    # Insert some sample data
    cur.execute("INSERT INTO ACTIVE_HABITS "
                "(HABIT_ID, HABIT_NAME, PERIODICITY, LAST_INCREMENTATION_DATE, STREAK_ONGOING) "
                "VALUES (1, 'Wake up at 6AM', 'Daily', '2023-02-23', 1), "
                "(2, 'Do 40 push-ups', 'Daily', '2023-02-23', 1), "
                "(3, 'Read your mail', 'Weekly', '2023-02-23', 1), "
                "(4, 'Pay your tuition fees', 'Monthly', '2023-02-23', 0), "
                "(5, 'Visit the dentist', 'Yearly', '2023-02-23', 0)"
                )

    cur.execute("INSERT INTO TRACKING_HABITS (EVENT_TIMESTAMP, HABIT_ID, EVENT_NAME) "
                "VALUES ('2023-02-23 05:28:41.806895',1,'Creation'), "
                "('2023-02-23 05:29:21.239371',2,'Creation'), "
                "('2023-02-23 05:30:34.029547',3,'Creation'), "
                "('2023-02-23 05:30:56.873206',4,'Creation'), "
                "('2023-02-23 05:31:17.899303',5,'Creation'), "
                "('2023-02-23 05:31:27.538606',1,'Incrementation'), "
                "('2023-02-23 05:31:40.354025',2,'Incrementation'), "
                "('2023-02-23 05:31:55.357245',3,'Incrementation')"
                )

    # Committing the commands to our database
    db.commit()

def add_habit(db, habit_name, habit_periodicity):
    """
    Based on the Tracker class, this method adds a habit to our database.
    Eventually, a message confirming the successful execution of the operation is displayed.
    :param db: a database
    :param habit_name: The name of the habit
    :param habit_periodicity: The periodicity of this habit
    :return: None
    """
    # Creating a Tracker object
    habit = Tracker(habit_name, habit_periodicity)
    values = habit.details

    # Updating the database
    cur = db.cursor()
    cur.execute("INSERT INTO ACTIVE_HABITS VALUES (?, ?, ?, ?)",
                (values[0], values[1], values[2], values[3]))
    cur.execute("INSERT INTO TRACKING_HABITS VALUES (?, ?, ?)",
                (datetime.datetime.now(), values[0], "Creation"))

    # Committing the commands to our database
    db.commit()

    # The habit was created
    print("Successfully created.")

def edit_habit(db, habit_id, column, new_value):
    cur = db.cursor()
    cur.execute(f"UPDATE ACTIVE_HABITS SET {column} = '{new_value}' WHERE HABIT_ID = {habit_id};")
    cur.execute("INSERT INTO TRACKING_HABITS VALUES (?, ?, ?)", (datetime.datetime.now(), habit_id, "Edition"))

    db.commit()

    print("Successfully edited.")

def increment_habit(db, habit_id):

    cur = db.cursor()

    cur.execute(f"UPDATE ACTIVE_HABITS "
                f"SET LAST_INCREMENTATION_DATE = {datetime.date.today()}, STREAK_ONGOING = 1 "
                f"WHERE HABIT_ID = {habit_id}")

    cur.execute("INSERT INTO TRACKING_HABITS VALUES (?, ?, ?)",
                (datetime.datetime.now(), habit_id, "Incrementation"))

    db.commit()

    print("Successfully incremented.")

def reset_habit(db, habit_id):
    cur = db.cursor()

    cur.execute(f"UPDATE ACTIVE_HABITS SET STREAK_ONGOING = 0 WHERE HABIT_ID = {habit_id}")
    cur.execute("INSERT INTO TRACKING_HABITS VALUES (?, ?, ?)", (datetime.datetime.now(), habit_id, "Resetting"))

    db.commit()

    print("Successfully reset.")

def delete_habit(db, habit_id, broken=False):
    # Starting a cursor object
    cur = db.cursor()

    # Retrieving the start date of the habit, which indicates the first time the habit was incremented by the user
    cur.execute(f"SELECT MIN(EVENT_TIMESTAMP) FROM TRACKING_HABITS "
                f"WHERE HABIT_ID = {habit_id} AND EVENT_NAME = 'INCREMENTATION'")
    start_date = cur.fetchone()[0]

    # Retrieving the end date of the habit, which indicates the last time the habit was incremented by the user
    cur.execute(f"SELECT MAX(EVENT_TIMESTAMP) FROM TRACKING_HABITS "
                f"WHERE HABIT_ID = {habit_id} AND EVENT_NAME = 'INCREMENTATION'")
    end_date = cur.fetchone()[0]

    # Backing-up data from the active habits table
    cur.execute("SELECT * FROM ACTIVE_HABITS WHERE HABIT_ID = ?", (habit_id,))
    data = list(cur.fetchone())

    # Deleting the data from the active habits table
    cur.execute("DELETE FROM ACTIVE_HABITS WHERE HABIT_ID = ?", (habit_id,))

    # Inserting data into the broken habits table
    cur.execute("INSERT INTO BROKEN_HABITS VALUES (?, ?, ?, ?, ?, ?)",
                (data[0], data[1], data[2], start_date, end_date, data[4])
                )

    # Updating the habits tracking table depending on the case
    if not broken:
        cur.execute("INSERT INTO TRACKING_HABITS VALUES (?, ?, ?)", (datetime.datetime.now(), habit_id, "Broken"))
        print(f"{data[0]} is broken due to not being incremented on time.")
    else:
        cur.execute("INSERT INTO TRACKING_HABITS VALUES (?, ?, ?)", (datetime.datetime.now(), habit_id, "Deletion"))
        print("Successfully deleted.")

    # Committing the changes to the database
    db.commit()

def show_habits_active(db):
    """
    Shows the records of active habits
    :param db: The database we're working with.
    :return: A dataframe.
    """
    # Retrieving data from a database
    cur = db.cursor()
    cur.execute("SELECT * FROM ACTIVE_HABITS ;")

    # Transforming data into a dataframe
    data = cur.fetchall()
    df = pd.DataFrame(data,
                      columns=['HABIT_ID', 'HABIT_NAME', 'PERIODICITY', 'START_DATE', 'STREAK_ONGOING']
                      ).set_index("HABIT_ID")

    return df

def show_habits_broken(db):
    """
    Shows the records of broken habits
    :param db: The database we're working with.
    :return: a dataframe.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM BROKEN_HABITS")

    # Transforming data into a dataframe
    data = cur.fetchall()
    df = pd.DataFrame(data,
                      columns=['HABIT_ID', 'HABIT_NAME', 'PERIODICITY', 'START_DATE', 'END_DATE', 'STREAK_ENDED']
                      ).set_index("HABIT_ID")

    return df

def habit_breaking_check(db):
    # Preparing  data
    df = show_habits_active(db).reset_index()
    frequencies = ["Daily", "Weekly", "Twice a month", "Monthly", "Quarterly", "Twice a year", "Yearly"]

    # Adjusting data to its adequate format
    df["START_DATE"] = df["START_DATE"].astype("datetime64")

    # Designing our functions
    def quarter_range(date):
        if date.month in range(1, 4):
            start_quarter = datetime.date(datetime.date.today().year, 1, 1)
            end_quarter = datetime.date(datetime.date.today().year, 3, 31)
            quarter = [start_quarter, end_quarter]
            return quarter
        elif date.month in range(4, 7):
            start_quarter = datetime.date(datetime.date.today().year, 4, 1)
            end_quarter = datetime.date(datetime.date.today().year, 6, 30)
            quarter = [start_quarter, end_quarter]
            return quarter
        elif date.month in range(7, 10):
            start_quarter = datetime.date(datetime.date.today().year, 7, 1)
            end_quarter = datetime.date(datetime.date.today().year, 9, 30)
            quarter = [start_quarter, end_quarter]
            return quarter
        else:
            start_quarter = datetime.date(datetime.date.today().year, 10, 1)
            end_quarter = datetime.date(datetime.date.today().year, 12, 31)
            quarter = [start_quarter, end_quarter]
            return quarter

    def semester_range(date):
        if date.month in range(1, 7):
            start_semester = datetime.date(datetime.date.today().year, 1, 1)
            end_semester = datetime.date(datetime.date.today().year, 6, 30)
            semester = [start_semester, end_semester]
            return semester
        else:
            start_semester = datetime.date(datetime.date.today().year, 7, 1)
            end_semester = datetime.date(datetime.date.today().year, 12, 31)
            semester = [start_semester, end_semester]
            return semester

    # Running our check
    for i in range(df.shape[0]):
        # Setting some basic variables
        habit_id = df.iloc[i, 0]
        periodicity = df.iloc[i, 2]
        last_incrementation_date = df.iloc[i, 3]
        year, week_num, day_of_week = datetime.date.today().isocalendar()

        if periodicity == frequencies[0]:
            if not last_incrementation_date == datetime.date.today():
                delete_habit(db, habit_id, broken=True)

        elif periodicity == frequencies[1]:
            start_date = datetime.date.fromisocalendar(year, week_num, 1)
            end_date = datetime.date.fromisocalendar(year, week_num, 7)

            if not start_date <= last_incrementation_date <= end_date:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == frequencies[2]:
            start_date = datetime.date.fromisocalendar(year, week_num, 1)
            end_date = datetime.date.fromisocalendar(year, week_num+1, 7)

            if not start_date <= last_incrementation_date <= end_date:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == frequencies[3]:
            if not last_incrementation_date.month == datetime.date.today().month:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == frequencies[4]:
            condition_1 = quarter_range(last_incrementation_date)[0] <= datetime.date.today()
            condition_2 = datetime.date.today() <= quarter_range(last_incrementation_date)[1]
            if not condition_1 and condition_2:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == frequencies[5]:
            condition_1 = semester_range(last_incrementation_date)[0] <= datetime.date.today()
            condition_2 = datetime.date.today() <= semester_range(last_incrementation_date)[1]
            if not condition_1 and condition_2:
                delete_habit(db, habit_id, broken=True)

        else:
            if not last_incrementation_date.year == datetime.date.today().year:
                delete_habit(db, habit_id, broken=True)

    return None
