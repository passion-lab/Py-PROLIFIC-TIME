# [#] Program Objectives:
# [>]
# [+] Docstrings to be added on each functions
# [+] Proper information, help, update labels to be included

# [i] Importing required modules
from datetime import datetime, timedelta
from pickle import load, dump
from time import sleep
from os import path, mkdir


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


# parent functions
def set_data(data: int, title: str, description: str = "A brief description",
             date: datetime.date = datetime.today().date(),  # [i] default date = Today
             time: datetime.time = (datetime.now() + timedelta(hours=1)).time(),  # [i] default time = Next hour
             from_time: datetime.time = None,
             to_time: datetime.time = None,
             remind: list[timedelta] = None,
             repeat: bool = False,
             frequency: str = None,
             from_data: datetime.date = None,
             to_data: datetime.date = None):
    if remind is None:
        # [i] default reminder = On time
        remind = [time]
    else:
        # [i] reminders to be added on user request from remind argument
        remind = [(datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S") - item).time() for item in remind]
        remind.insert(0, time)

    data = _data_type(data)
    timestamp = datetime.now()

    data[0]['data'].append({
        "created": timestamp,  # auto event creation timestamp for sorting purposes
        "title": title,
        "description": description,
        "when": {
            "date": date if not frequency else None,
            "time": time
        },
        "period": {
            "start_time": from_time,
            "end_time": to_time
        } if data[1] != 'reminder' else None,
        "reminder": remind,
        "repeat": repeat,
        "loop": {
            "how_frequent": frequency,  # [+] to be fun
            "start_date": from_data,
            "end_date": to_data
        } if repeat else None
    })

    data[0]['count'] += 1

    # [i] updates the local database shortly
    with open("Database/" + data[2], "wb") as f:
        dump(data[0], f)


def get_data(data: int, index: int = None, _blank: bool = False):
    data = _data_type(data)

    if _blank:
        for index, option in enumerate(options):
            data = _data_type(index + 1)
            if data[0]['count'] != 0:
                break
        else:
            # [i] Start-up line (basically used while database is empty)
            print(" - You are new here. Please add some event to be more productive. - ")
    else:
        if data[0]['count'] == 0:
            if index != 0:
                print("You've no", data[1], "yet! Please add some", data[1], "first.")
        else:
            print("You've {} {}{} so far:".format(data[0]['count'], data[1], "s" if data[0]['count'] > 1 else ""))
            if len(data[0]['data']) != 0:
                for index, item in enumerate(data[0]['data']):
                    print(f" {str(index + 1)}. {item['title']}")


def del_data(data: int, index: int):
    data = _data_type(data)

    print(f"Are you sure you want to delete the {data[1]}?")
    permission = input("Press 'N' to go back and 'Enter' to delete: ").strip().upper()
    data[0]['data'].pop(index - 1) if permission != "N" else None

    data[0]['count'] -= 1

    # [i] updates the local database shortly
    with open("Database/" + data[2], "wb") as f:
        dump(data[0], f)


def mod_data(data: int, index: int):
    pass


# child functions
def _remind(data: int):
    pass


def _data_type(data: int):
    for index, option in enumerate(options):
        if data == index + 1:
            # [i] List of main event variables, event names (singular), event database file names
            return globals()[option], option[:-1], option[:-1] + ".data"


def _data_update(method: str = 'PUSH'):
    if method == 'PUSH':
        for index, option in enumerate(options):
            data = _data_type(index + 1)
            with open("Database/" + data[2], "wb") as f:
                dump(data[0], f)

    elif method == 'PULL':
        for index, option in enumerate(options):
            data = _data_type(index + 1)
            with open("Database/" + data[2], "rb") as f:
                globals()[option] = load(f)


# independent program functions
def __input_validation(message: str, valid: list = None, _any: bool = False):
    selection = input(message).strip().lower()

    if _any:
        if selection:
            return selection
        else:
            print("You've to enter something before proceeding. Please try again.")
            __input_validation(message, _any=True)
    else:
        if selection in valid:
            return selection
        else:
            print("Invalid input. Please try again.")
            __input_validation(message, valid)


def __date_time():
    pass


if __name__ == '__main__':

    # day, month, year = [int(i) for i in input("Date (dd/mm/yyyy): ")]
    # hour, minute, second = [int(i) for i in input("Date (hh:mm:ss): ")]

    if path.isdir("Database"):
        # [i] updates the local database shortly
        # for sl, event in enumerate(options):
        #     root = _data_type(sl + 1)
        #     with open("Database/" + root[2], "rb") as file:
        #         globals()[event] = load(file)
        _data_update(method='PULL')

    else:
        mkdir("Database")
        # # [i] updates the local database shortly
        # for sl, event in enumerate(options):
        #     root = _data_type(sl + 1)
        #     with open("Database/" + root[2], "wb") as file:
        #         dump(root[0], file)
        _data_update(method='PUSH')

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

    # for i in range(1, 5):
    #     get_data(i, 0)

    # print("\r")
    # set_data(3, "First")
    set_data(4, "First")
    # set_data(4, "Second")
    # set_data(2, "Second")

    # del_data(4, 2)

    for i in range(1, 5):
        get_data(i, 0)

    print("Welcome to the Task Management Software")
    get_data(0, _blank=True)

    while True:
        print("Your options are:\n  [1] Add Event\n  [2] Show Event List\n  [3] Delete Event\n  [4] Modify Event\n")
        user_option = __input_validation("What do you want to do? [Press '^E' to exit]", [str(range(1, 5))])

        if user_option == "1":
            # [i] Add event data
            print("Events are:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            user_event = int(__input_validation("What do you want to add? ", [str(range(1, 5))]))

            user_event_title = __input_validation(f"Enter a title = ")
            user_event_description = __input_validation(f"Add a brief note for your {_data_type(user_event + 1)[1]} = ")

            user_event_date = None
            while 1:
                try:
                    user_event_date = input("Event date (dd/mm/yyyy) = ")
                    user_event_date = datetime.date(datetime.strptime(user_event_date, "%d/%m/%Y"))
                    if user_event_date >= datetime.now().date():
                        break
                    else:
                        print("Sorry, you've to go for the same day or a later day. Try again.")

                except ValueError:
                    print("Wrong input! Enter date correctly again.")
                    continue
            user_event_time = None
            while 1:
                try:
                    user_event_time = input("Event time (hh:mm:ss) = ")
                    user_event_time = datetime.time(datetime.strptime(user_event_time, "%H:%M:%S"))
                    if user_event_time > datetime.now().time():
                        break
                    else:
                        print("Sorry, you've to go for the a later time. Try again.")

                except ValueError:
                    print("Wrong input! Enter time correctly again.")
                    continue

            set_data(user_event, title=user_event_title, description=user_event_description, date=user_event_date,
                     time=user_event_time)

        elif user_option == "2":
            # [i] Show event list
            pass

        elif user_option == "3":
            # [i] Delete event
            pass

        elif user_option == "4":
            # [i] Modify event
            pass

        elif user_option == "^E":
            # [i] Exit node
            exit()
