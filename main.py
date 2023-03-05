from db import get_db, show_habits_active, show_habits_broken, habit_breaking_check
from db import add_habit, increment_habit, edit_habit, reset_habit, delete_habit
from analysis import show_habits_with_same_periodicity, show_longest_streak_of_a_habit, show_longest_streak
import questionary

def cli():
    db = get_db()

    print("=========================================================================")
    print("|                                                                       |")
    print("|            The Habits Tracker app, powered by IU Hochshule.           |")
    print("|                                                                       |")
    print("=========================================================================")

    habit_breaking_check(db)

    while True:

        choice = questionary.select('What do you want to do ?',
                                    choices=["Analyze", "Create", "Edit", "Increment", "Reset", "Delete", "Exit"]
                                    ).ask()

        if choice == "Analyze":

            while True:

                choice = questionary.select("What would you like to see?",
                                            choices=['Show active habits',
                                                     'Show broken habits history',
                                                     'Show habits with the same periodicity',
                                                     'Show the longest streak of a habit',
                                                     'Show the longest streak ever made']
                                            ).ask()

                if choice == 'Show active habits':
                    print(show_habits_active(db))

                    # In case, the user want to exit the loop from here
                    question = questionary.confirm("Anything else").ask()
                    if not question:
                        break

                elif choice == 'Show broken habits history':
                    print(show_habits_broken(db))

                    # In case, the user want to exit the loop from here
                    question = questionary.confirm("Anything else").ask()
                    if not question:
                        break

                elif choice == 'Show habits with the same periodicity':
                    periodicity = questionary.select("Choose the periodicity :",
                                                     choices=["Daily", "Weekly", "Twice a month", "Monthly",
                                                              "Quarterly", "Twice a year", "Yearly"]).ask()
                    show_habits_with_same_periodicity(db, periodicity)

                    # In case, the user want to exit the loop from here
                    question = questionary.confirm("Anything else").ask()
                    if not question:
                        break

                elif choice == 'Show the longest streak of a habit':
                    habit_name = questionary.select("What's the name of this habit",
                                                    choices=["1", "2", "3"]
                                                    ).ask()
                    print(show_longest_streak_of_a_habit(db, habit_name))

                    # In case, the user want to exit the loop from here
                    question = questionary.confirm("Anything else").ask()
                    if not question:
                        break

                elif choice == 'Show the longest streak ever made':
                    print(show_longest_streak(db))

                    # In case, the user want to exit the loop from here
                    question = questionary.confirm("Anything else").ask()
                    if not question:
                        break

                else:
                    pass

        elif choice == "Create":
            name = questionary.text("What is the name of this habit:").ask()
            periodicity = questionary.select("How frequent are you willing to do this habit?",
                                             choices=["Daily", "Weekly", "Twice a month", "Monthly",
                                                      "Quarterly", "Twice a year", "Yearly"]).ask()
            add_habit(db, name, periodicity)

            # In case, the user want to exit the loop from here
            question = questionary.confirm("Anything else?").ask()
            if not question:
                print("We'll miss you here, comeback soon!")
                break

        elif choice == "Edit":
            print(show_habits_active(db))
            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()

            column = questionary.select("Great, what are you going to change?",
                                        choices=['HABIT_NAME', 'PERIODICITY']
                                        ).ask()

            if column == "FREQUENCY":
                new_value = questionary.select("Almost there, choose the frequency you want",
                                               choices=["Daily", "Weekly", "Twice a month", "Monthly",
                                                        "Quarterly", "Twice a year", "Yearly"]).ask()

            else:
                new_value = questionary.text("Almost there, type in what do you want").ask()

            edit_habit(db, habit_id, column, new_value)

            # In case, the user want to exit the loop from here
            question = questionary.confirm("Anything else").ask()
            if not question:
                print("We'll miss you here, comeback soon!")
                break

        elif choice == "Increment":
            print(show_habits_active(db))
            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()

            increment_habit(db, habit_id)

            # In case, the user want to exit the loop from here
            question = questionary.confirm("Anything else").ask()
            if not question:
                print("We'll miss you here, comeback soon!")
                break

        elif choice == "Reset":
            print(show_habits_active(db))
            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()
            reset_habit(db, habit_id)

            # In case, the user want to exit the loop from here
            question = questionary.confirm("Anything else").ask()
            if not question:
                print("We'll miss you here, comeback soon!")
                break

        elif choice == "Delete":
            print(show_habits_active(db))
            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()
            delete_habit(db, habit_id)

            # In case, the user want to exit the loop from here
            question = questionary.confirm("Anything else").ask()
            if not question:
                print("We'll miss you here, comeback soon!")
                break

        elif choice == "Exit":
            print("We'll miss you here, comeback soon!")
            break


if __name__ == "__main__":
    cli()
