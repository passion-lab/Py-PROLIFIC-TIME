# [i] Importing required modules
# from datetime import datetime, timedelta
# from pickle import load, dump
from main import *


# from NotificationHandler import *
# from Engine import *


# parent functions
def set_data(data: int,
             date: datetime.date,
             time: datetime.time,
             title: str,
             description: str = "A brief description",
             from_datetime: datetime = None,
             to_datetime: datetime = None,
             remind: list[timedelta] = None,
             repeat: bool = False,
             frequency: str = None,
             from_date: datetime.date = None,
             next_date: datetime.date = None,
             to_date: datetime.date = None):
    if remind is None:
        # [i] default reminder = On time
        remind = [time]
    else:
        # [i] reminders to be added on user request from remind argument
        remind = [(datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S") - option).time() for option in remind]
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
        "period": {
            "start_datetime": from_datetime,
            "end_datetime": to_datetime
        } if data[1] == 'task' else None,
        "reminder": remind,
        "repeat": repeat,
        "loop": {
            "how_frequent": frequency,
            "start_date": from_date,
            "next_date": next_date,
            "end_date": to_date
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


def del_data(data: int, index, _prompt: bool = True):
    data = data_type_(data)

    if _prompt:
        print(f"Are you sure you want to delete the {data[1]}?")
        # permission = input().strip()
        permission = input_validation__("Press 'Y' to delete or 'Enter' to go back: ", ['Y', ''])
        if permission == "Y":
            if type(index) == int:
                data[0]['data'].pop(index - 1)
                data[0]['count'] -= 1
            else:
                data[0]['data'].clear()
                data[0]['count'] = 0

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
    data = data_type_(data)
    for key in data[0]['data'][index - 1]:
        val = data[0]['data'][index - 1][key]
        if type(val) == dict:
            for sub_key in val:
                print("  {:>12} = {}".format(sub_key.title(), val[sub_key]))
        elif type(val) == list:
            for index, sub_val in enumerate(val):
                print("  {:>12} = {}".format(key.title() if index == 0 else "", sub_val))
        elif type(val) == bool:
            val = "Yes" if val else "No"
            print("  {:>12} = {}".format(key.title(), val))
        elif val is None:
            val = "Yes" if val else "No"
            print("  {:>12} = {}".format(key.title(), val))
        else:
            print("  {:>12} = {}".format(key.title(), val))


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


if __name__ == '__main__':
    print("SORRY! It's not the main program file."
          "\nIt's the Event manipulation file associated with the main program."
          "\n\nPlease run the 'main.py' file for the main program!")
