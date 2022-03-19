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
             date: datetime.date = None,
             time: datetime.time = None,
             from_time: datetime.time = None,
             to_time: datetime.time = None,
             remind: list[timedelta] = None,
             repeat: bool = False,
             frequency: str = None,
             from_data: datetime.date = None,
             to_data: datetime.date = None):

    if date is None:
        # [i] default date = Today
        date = datetime.today().date()

    if time is None:
        # [i] default time = Next hour
        time = (datetime.now() + timedelta(hours=1)).time()

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
                # [i] Returns True if data exists
                return True
        else:
            # [i] Start-up line (basically used while database is empty)
            print(" - You are new here. Please add some event to be more productive. - ")
    else:
        if data[0]['count'] == 0:
            if index != 0:
                # [i] Printing absence of data
                print("You've no", data[1], "yet! Please add some", data[1], "first.")
        else:
            # [i] Printing existing data
            print("You've {} {}{} so far:".format(data[0]['count'], data[1], "s" if data[0]['count'] > 1 else ""))
            if len(data[0]['data']) != 0:
                for index, info in enumerate(data[0]['data']):
                    print(f" {str(index + 1)}. {info['title']} [{info['when']['date']} {info['when']['time']}]")
                return data[0]['count']


def del_data(data: int, index: int):
    data = _data_type(data)

    print(f"Are you sure you want to delete the {data[1]}?")
    # permission = input().strip()
    permission = __input_validation("Press 'Y' to delete or 'Enter' to go back: ", ['Y', ''])
    if permission == "Y":
        data[0]['data'].pop(index - 1)
        data[0]['count'] -= 1

        # [i] updates the local database shortly
        with open("Database/" + data[2], "wb") as f:
            dump(data[0], f)
            print("Event successfully deleted!")


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
    """

    :param message: Message/Question to ask the user to collect their input
    :param valid: A list of possible options (in raw format) to verify user input.
    :param _any: To assure that the user can enter anything or not leave blank. valid parameter will become invalid here.
    :return: Returns user input as raw format
    """
    selection = input(message).strip()
    # [i] Convert user input into integer if it was digit else as it was
    selection = int(selection) if selection.isdigit() else selection

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

    if path.isdir("Database"):
        _data_update(method='PULL')

    else:
        mkdir("Database")
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
    # set_data(4, "First")
    # set_data(4, "Second")
    # set_data(2, "Second")

    # del_data(4, 2)

    print("Welcome to the Task Management Software")
    value = get_data(0, _blank=True)
    if value:
        # [i] Displaying events if get_data returns True
        for i in range(1, 5):
            get_data(i, 0)

    while True:
        # [+] Advance option to be added for database management...
        print("Your options are:\n  [1] Add Event\n  [2] Show Event List\n  [3] Delete Event\n  [4] Modify Event")
        user_option = __input_validation("What do you want to do? [Press '^E' to exit] ", ["^E", 1, 2, 3, 4])

        # [i] Add event data
        if user_option == 1:
            print("Add:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            # [i] Collecting user parameters
            user_event = __input_validation("What do you want to add? ", [i for i in range(1, 5)])
            user_event_title = __input_validation(f"Enter a title = ", _any=True)
            user_event_description = input(f"Add a brief note for your {_data_type(user_event)[1]} "
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
            _data_update(method='PULL')
            for i in range(1, 5):
                get_data(i, 0)

        # [i] Delete event
        elif user_option == 3:
            print("Delete:")
            for sl, item in enumerate(options):
                print(f"  [{sl + 1}] - {item.title()[:-1]}")
            user_event = __input_validation("From which? ", [i for i in range(1, 5)])
            number = get_data(user_event)
            if number:
                user_entry = __input_validation("Choose an event to delete: ", [i for i in range(1, number + 1)])
                # print(user_entry, type(user_entry))
                del_data(user_event, user_entry)

                # [i] Show event list after deletion
                _data_update(method='PULL')
                for i in range(1, 5):
                    get_data(i, 0)

        # [i] Modify event
        elif user_option == 4:
            pass

        # [i] Exit node
        elif user_option == "^E":
            exit()
