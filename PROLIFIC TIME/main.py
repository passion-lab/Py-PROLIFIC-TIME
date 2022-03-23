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
countdowns, reminders, tasks, todos = [{
    "count": 0,
    # imposed by the program on user demand...
    "data": []
}] * 4


# reminders = {
#     "count": 0,
#     # imposed by the program on user demand...
#     "data": []
# }
# tasks = {
#     "count": 0,
#     # imposed by the program on user demand...
#     "data": []
# }
# todos = {
#     "count": 0,
#     # imposed by the program on user demand...
#     "data": []
# }

# [i] Additional reminders


def input_datetime__(what: str, event_date: datetime.date):
    """

    :param what: What to receive? 'DATE' or 'TIME
    :param event_date: A date is required to troubleshoot the time
    :return: Date or Time in datetime format
    """

    if what == 'DATE':
        while 1:
            try:
                event_date = input("Event date [default today; dd/mm/yyyy] = ")
                if event_date:
                    event_date = datetime.date(datetime.strptime(event_date, "%d/%m/%Y"))
                    # [i] Taking date only if it is today or a later day
                    if event_date >= datetime.now().date():
                        return event_date
                    else:
                        print("Sorry, you've to go for the same day or a later day. Try again.")
                else:
                    # [i] default date = Today
                    return datetime.today().date()
            except ValueError:
                print("Wrong input! Enter date correctly again.")
                continue

    if what == 'TIME':
        while 1:
            try:
                event_time = input("Event time [default next hour; hh:mm:ss] = ")
                if event_time:
                    event_time = datetime.time(datetime.strptime(event_time, "%H:%M:%S"))
                    # [i] Taking time only if it is after the current time
                    if event_date == datetime.now().date() and event_time <= datetime.now().time():
                        print("Sorry, you've to go for the a later time. Try again.")
                    else:
                        return event_time
                else:
                    # [i] default time = Next hour
                    return (datetime.now() + timedelta(hours=1)).time()
            except ValueError:
                print("Wrong input! Enter time correctly again.")
                continue


def input_reminder__():
    _reminds_at = []
    while True:
        __0 = input_validation__("['>>' Skip] Want to create more reminders? ", [">>", "Y", "y"], default="Y")
        if __0 == ">>":
            break
        print("How will we remind you to '{}' ? It may be before,\n"
              "  [1]  5 mins;  [2]  10 mins;  [3]  15 mins;  [4] 30 mins;  [5] 45 mins\n"
              "  [6]  1 hour;  [7]  3 hours;  [8]  6 hours;  [9] 12 hours\n"
              "  [10] 1 day;   [11] 3 days;   [12] 5 days\n"
              "  [13] 1 week;  [14] 1 month;  [15] 1 year".format(user_event_title))
        __selection = input_validation__("['>' Custom] Set reminder for = ", [i for i in range(1, 16)], default=6)
        if __selection == ">":
            _w, _d, _h, _m, _s = [0] * 5
            while 1:
                try:
                    _w, _d, _h, _m, _s = input("How long? [Weeks:Days:Hours:Minutes:Seconds] = ").strip().split(":")
                    _w, _d, _h, _m, _s = int(_w), int(_d), int(_h), int(_m), int(_s)
                    break
                except ValueError:
                    print("Wrong input! Integer numbers have to input separated by ':' and put '0' for no value.")
                    continue
            _reminds_at.append(timedelta(weeks=_w, days=_d, hours=_h, minutes=_m, seconds=_s))
        elif __selection == 1:
            _reminds_at.append(timedelta(minutes=5))
        elif __selection == 2:
            _reminds_at.append(timedelta(minutes=10))
        elif __selection == 3:
            _reminds_at.append(timedelta(minutes=15))
        elif __selection == 4:
            _reminds_at.append(timedelta(minutes=30))
        elif __selection == 5:
            _reminds_at.append(timedelta(minutes=45))
        elif __selection == 6:
            _reminds_at.append(timedelta(hours=1))
        elif __selection == 7:
            _reminds_at.append(timedelta(hours=3))
        elif __selection == 8:
            _reminds_at.append(timedelta(hours=6))
        elif __selection == 9:
            _reminds_at.append(timedelta(hours=12))
        elif __selection == 10:
            _reminds_at.append(timedelta(days=1))
        elif __selection == 11:
            _reminds_at.append(timedelta(days=3))
        elif __selection == 12:
            _reminds_at.append(timedelta(days=5))
        elif __selection == 13:
            _reminds_at.append(timedelta(weeks=1))
        elif __selection == 14:
            _reminds_at.append(timedelta(weeks=4))
        elif __selection == 15:
            _reminds_at.append(timedelta(weeks=52))
    return _reminds_at if len(_reminds_at) >= 1 else None


def input_recurrence__():
    selection = input_validation__("")


# independent program functions
def input_validation__(message: str, valid: list = None, default=None, _any: bool = False):
    """

    :param message: Message/Question to ask the user to collect their input
    :param valid: A list of possible options (in raw format) to verify user input.
    :param default: Default value if user press enter only without inputting anything or space
    :param _any: To assure that the user can enter anything or not leave blank. valid parameter will become invalid here.
    :return: Returns user input as raw format
    """
    while True:
        selection = input(message).strip()
        # [i] Convert user input into integer if it was digit else as it was
        selection = int(selection) if selection.isdigit() else selection

        if _any:
            if selection:
                return selection
            else:
                print("You've to enter something before proceeding. Please try again.")
                input_validation__(message, _any=True)
        else:
            if default is not None and not selection:
                return default
            elif selection in valid:
                return selection
            else:
                print("Invalid input. Please try again.")


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
        for sl, _ in enumerate(options):
            get_data(sl + 1, 0)

    while True:
        # [+] Advance option to be added for database management...
        print("Your options are:\n  [1] Add Event\n  [2] Show Event List\n  [3] Delete Event\n  [4] Modify Event")
        user_option = input_validation__("What do you want to do? [Press '^E' to exit] ",
                                         ["^E"] + [sl + 1 for sl, _ in enumerate(options)])

        # [i] Add event data
        if user_option == 1:
            print("Add:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            # [i] Collecting user parameters
            user_event = input_validation__("What do you want to add? ['<' Back] ",
                                            ["<"] + [sl + 1 for sl, _ in enumerate(options)])
            if user_event == "<":
                continue
            user_event_title = input_validation__(f" [REQUIRED] Enter a title = ", _any=True)
            user_event_de_sription = input(f"[Optional] Add a brief note for your {data_type_(user_event)[1]} = ")
            user_event_date = input_datetime__('DATE', None)
            user_event_time = input_datetime__('TIME', user_event_date)
            if data_type_(user_event)[1] == "task":
                user_event_period = input_validation__(f"[Default Yes; 'N' No] Add a span for your task = "
                                                       f"'{user_event_title}'? ", ["N", "n", "Y", "y"], default="Y")
                if user_event_period.upper() == "N":
                    pass
                else:
                    user_event_datetime = datetime(user_event_date.year, user_event_date.month, user_event_date.day,
                                                   user_event_time.hour, user_event_time.minute, user_event_time.second)
                    w, d, h, m, s = [0] * 5  # [i] Initiating 0 values all for week, day, hour, minute, and second
                    while 1:
                        try:
                            w, d, h, m, s = input("How long? [Weeks:Days:Hours:Minutes:Seconds] = ").strip().split(":")
                            w, d, h, m, s = int(w), int(d), int(h), int(m), int(s)
                            break
                        except ValueError:
                            print("Wrong input! Please enter all integer values separated by ':' for each variables "
                                  "and '0' for None.")
                            continue
                    user_event_until = user_event_datetime + timedelta(weeks=w, days=d, hours=h, minutes=m, seconds=s)
                    if user_event_datetime == user_event_until:
                        user_event_until = None
            user_event_reminder = input_reminder__()

            # [i] Adding event to the database
            set_data(user_event, title=user_event_title, de_sription=user_event_de_sription, date=user_event_date,
                     time=user_event_time, remind=user_event_reminder)

            # [i] Displaying events after adding
            for sl, _ in enumerate(options):
                get_data(sl + 1, 0)

        # [i] Show event list
        elif user_option == 2:
            data_update_(method='PULL')
            for sl, _ in enumerate(options):
                get_data(sl + 1, 0)

        # [i] Delete event
        elif user_option == 3:
            print("Delete:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            user_event = input_validation__("From which? ['<' Back] ", ["<"] + [sl + 1 for sl, _ in enumerate(options)])
            if user_event == "<":
                continue
            number = get_data(user_event)
            if number:
                user_entry = input_validation__("Choose an event to delete: ", [i for i in range(1, number + 1)])
                # print(user_entry, type(user_entry))
                del_data(user_event, user_entry)

                # [i] Show event list after deletion
                data_update_(method='PULL')
                for sl, _ in enumerate(options):
                    get_data(sl + 1, 0)

        # [i] Modify event
        elif user_option == 4:
            print("Modify:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            # [i] Show a list of all entries from each events
            user_event = input_validation__("From which? ['<' Back] ", ["<"] + [sl + 1 for sl, _ in enumerate(options)])
            if user_event == "<":
                continue
            number = get_data(user_event)
            if number:
                user_entry = input_validation__("Choose an event to delete: ", [i for i in range(1, number + 1)])
                mod_data(user_event, user_entry)
                print("Options:\n  [1] Edit\n  [2] Delete")
                user_edit = input_validation__("What do you want? ['<' Back] ", ["<", 1, 2])
                if user_edit == 1:
                    pass
                elif user_edit == 2:
                    del_data(user_event, user_entry)

                    # [i] Show event list after deletion
                    data_update_(method='PULL')
                    for sl, _ in enumerate(options):
                        get_data(sl + 1, 0)
                else:
                    continue

        # [i] Exit node
        elif user_option == "^E":
            exit()
