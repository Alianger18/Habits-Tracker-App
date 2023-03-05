from db import show_habits_active, show_habits_broken

def show_habits_with_same_periodicity(db, habit_periodicity):
    df = show_habits_active(db)
    if habit_periodicity in list(df["PERIODICITY"].values):
        df_periodicity = df[df["PERIODICITY"] == habit_periodicity]
        print(df_periodicity)
    else:
        print("Sorry, there's currently no habit with the specified periodicity.")

def show_longest_streak(db):
    df_active = show_habits_active(db)
    df_broken = show_habits_broken(db)

    longest_streak_active = df_active.loc[df_active["STREAK_ONGOING"].idxmax()]
    longest_streak_broken = df_broken.loc[df_broken["STREAK_ENDED"].idxmax()]

    if longest_streak_active["STREAK_ONGOING"] > longest_streak_broken["STREAK_ENDED"]:
        print(longest_streak_active)
    else:
        print(longest_streak_broken)

def show_longest_streak_of_a_habit(db, habit_name):
    df_active = show_habits_active(db)
    df_broken = show_habits_broken(db)

    longest_streak_active = df_active[df_active["HABIT_NAME"] == habit_name]["STREAK_ONGOING"].idxmax()
    longest_streak_broken = df_broken[df_broken["HABIT_NAME"] == habit_name]["STREAK_ENDED"].idxmax()

    if longest_streak_active["STREAK_ONGOING"] > longest_streak_broken["STREAK_ENDED"]:
        print(longest_streak_active)
    else:
        print(longest_streak_broken)
