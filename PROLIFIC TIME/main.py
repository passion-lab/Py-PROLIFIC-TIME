# [#] Program Objectives:
# [>]
# [+] Docstrings to be added on each functions
# [+] Proper information, help, update labels to be included

# # [i] Importing required modules
from datetime import datetime, timedelta
from pickle import load, dump
from os import path, mkdir
from EventData import *
# from NotificationHandler import *
# from Engine import *


# [i] List of available event options
# [!] WARNING: It's the Main list, change here must affect the whole program
options = ["countdowns", "reminders", "tasks", "todos"]


# [i] Default empty dictionaries for each events for initial database
countdowns = {
    "count": 0,
    # imposed by the program on user demand...
    "data": []
}
reminders = {
    "count": 0,
    # imposed by the program on user demand...
    "data": []
}
tasks = {
    "count": 0,
    # imposed by the program on user demand...
    "data": []
}
todos = {
    "count": 0,
    # imposed by the program on user demand...
    "data": []
}


def __date_time():
    pass


if __name__ == '__main__':

    if path.isdir("Database"):
        data_update_(method='PULL')

    else:
        mkdir("Database")
        data_update_(method='PUSH')

    """
    dt = input("Date (dd/mm/yyyy): ")
    dt = datetime.date(datetime.strptime(dt, "%d/%m/%Y"))
    tm = input("Time (hh:mm:ss): ")
    tm = datetime.time(datetime.strptime(tm, "%H:%M:%S"))

    set_data(1, "First", "My first countdown")
    set_data(1, "Second", date=dt, repeat=True, remind=[timedelta(minutes=30), timedelta(hours=1)])
    set_data(1, "Third", "A brief note", repeat=False, date=dt, time=tm)
    set_data(3, "First", time=tm)
    set_data(2, "First")
    """

    print("Welcome to the Task Management Software")
    value = get_data(0, _blank=True)
    if value:
        # [i] Displaying events if get_data returns True
        for i in range(1, 5):
            get_data(i, 0)

    while True:
        # [+] Advance option to be added for database management...
        print("Your options are:\n  [1] Add Event\n  [2] Show Event List\n  [3] Delete Event\n  [4] Modify Event")
        user_option = input_validation__("What do you want to do? [Press '^E' to exit] ", ["^E", 1, 2, 3, 4])

        # [i] Add event data
        if user_option == 1:
            print("Add:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            # [i] Collecting user parameters
            user_event = input_validation__("What do you want to add? ", [i for i in range(1, 5)])
            user_event_title = input_validation__(f"Enter a title = ", _any=True)
            user_event_description = input(f"Add a brief note for your {data_type_(user_event)[1]} "
                                           f"[Leave empty for default] = ")
            user_event_date = None
            while 1:
                try:
                    user_event_date = input("Event date [default today; dd/mm/yyyy] = ")
                    if user_event_date:
                        user_event_date = datetime.date(datetime.strptime(user_event_date, "%d/%m/%Y"))
                        # [i] Taking date only if it is today or a later day
                        if user_event_date >= datetime.now().date():
                            break
                        else:
                            print("Sorry, you've to go for the same day or a later day. Try again.")
                    else:
                        user_event_date = None
                        break
                except ValueError:
                    print("Wrong input! Enter date correctly again.")
                    continue
            user_event_time = None
            while 1:
                try:
                    user_event_time = input("Event time [default next hour; hh:mm:ss] = ")
                    if user_event_time:
                        user_event_time = datetime.time(datetime.strptime(user_event_time, "%H:%M:%S"))
                        # [i] Taking time only if it is after the current time
                        if user_event_date == datetime.now().date() and user_event_time <= datetime.now().time():
                            print("Sorry, you've to go for the a later time. Try again.")
                        else:
                            break
                    else:
                        user_event_time = None
                        break
                except ValueError:
                    print("Wrong input! Enter time correctly again.")
                    continue

            # [i] Adding event to the database
            set_data(user_event, title=user_event_title, description=user_event_description, date=user_event_date,
                     time=user_event_time)

            # [i] Displaying events after adding
            for i in range(1, 5):
                get_data(i, 0)

        # [i] Show event list
        elif user_option == 2:
            data_update_(method='PULL')
            for i in range(1, 5):
                get_data(i, 0)

        # [i] Delete event
        elif user_option == 3:
            print("Delete:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            user_event = input_validation__("From which? ", [i for i in range(1, 5)])
            number = get_data(user_event)
            if number:
                user_entry = input_validation__("Choose an event to delete: ", [i for i in range(1, number + 1)])
                # print(user_entry, type(user_entry))
                del_data(user_event, user_entry)

                # [i] Show event list after deletion
                data_update_(method='PULL')
                for i in range(1, 5):
                    get_data(i, 0)

        # [i] Modify event
        elif user_option == 4:
            pass

        # [i] Exit node
        elif user_option == "^E":
            exit()
