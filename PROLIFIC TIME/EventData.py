# [i] Importing required modules
# from datetime import datetime, timedelta
# from pickle import load, dump
from main import *
# from NotificationHandler import *
# from Engine import *


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

    data = data_type_(data)
    timestamp = datetime.now()

    data[0]['data'].append({
        "created": timestamp,  # auto event creation timestamp for sorting purposes
        "title": title,
        "description": description,
        "when": {
            "date": date if not repeat else None,
            "time": time
        },
        # [i] Optional
        "period": {
            "start_time": from_time,
            "end_time": to_time
        } if data[1] == 'task' else None,
        "reminder": remind,
        "repeat": repeat,
        "loop": {
            "how_frequent": frequency,  # [+] to be fun
            # [i] Optional
            "start_date": from_data,
            "end_date": to_data
        } if repeat else None
    })

    data[0]['count'] += 1

    # [i] updates the local database shortly
    with open("Database/" + data[2], "wb") as f:
        dump(data[0], f)


def get_data(data: int, index: int = None, _blank: bool = False):
    data = data_type_(data)

    if _blank:
        for index, option in enumerate(options):
            data = data_type_(index + 1)
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


def del_data(data: int, index: int, _prompt: bool = True):
    data = data_type_(data)

    if _prompt:
        print(f"Are you sure you want to delete the {data[1]}?")
        # permission = input().strip()
        permission = input_validation__("Press 'Y' to delete or 'Enter' to go back: ", ['Y', ''])
        if permission == "Y":
            data[0]['data'].pop(index - 1)
            data[0]['count'] -= 1

            # [i] updates the local database shortly
            with open("Database/" + data[2], "wb") as f:
                dump(data[0], f)
                print("Event successfully deleted!")
    else:
        data[0]['data'].pop(index)
        data[0]['count'] -= 1

        # [i] updates the local database shortly
        with open("Database/" + data[2], "wb") as f:
            dump(data[0], f)
            print("Event successfully deleted!")


def mod_data(data: int, index: int):
    pass


# child functions
def remind_(data: int):
    pass


def data_type_(data: int):
    for index, option in enumerate(options):
        if data == index + 1:
            # [i] List of main event variables, event names (singular), event database file names
            return globals()[option], option[:-1], option[:-1] + ".data"


def data_update_(method: str = 'PUSH'):
    if method == 'PUSH':
        for index, option in enumerate(options):
            data = data_type_(index + 1)
            with open("Database/" + data[2], "wb") as f:
                dump(data[0], f)

    elif method == 'PULL':
        for index, option in enumerate(options):
            data = data_type_(index + 1)
            with open("Database/" + data[2], "rb") as f:
                globals()[option] = load(f)


# independent program functions
def input_validation__(message: str, valid: list = None, _any: bool = False):
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
            input_validation__(message, _any=True)
    else:
        if selection in valid:
            return selection
        else:
            print("Invalid input. Please try again.")
            input_validation__(message, valid)


if __name__ == '__main__':
    print("SORRY! It's not the main program file."
          "\nIt's the Event manipulation file associated with the main program."
          "\n\nPlease run the 'main.py' file for the main program!")
