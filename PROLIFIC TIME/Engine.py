# [i] Main Program Engine
# from main import *
from EventData import *
# from NotificationHandler import *
from plyer import notification
from datetime import datetime
from time import sleep
from threading import Thread

# [i] Get all saved data from all local databases
data_update_(method='PULL')

# [i] Creating an empty list and updating with the active entries from 4 events
# viz., countdown, reminder, task and todo
active_event = []

# [i] Creating an empty list and updating with the running entries
active_entry = []


def prt():
    print("Logging realtime data...")
    count = 0
    while 1:
        print(count, f":--- [Active Event]_{datetime.now().time()}")
        for entry in active_event:
            print(" >", entry['title'])
        print()

        print(count, f":--- [Active Entry]_{datetime.now().time()}")
        for entry in active_entry:
            print(" >", entry['title'])
        print()

        count += 5
        sleep(5)


# [i] Function to sync data from databases
def event_engine():
    print("Keeping an eay for tracking changes...")
    global active_event

    # [i] Runs an infinite loop
    while True:
        # [i] Continuously checking for new entry on each iteration
        data_update_(method='PULL')
        # for index, option in options:
        # [i] Collecting the data
        data = data_type_(1)
        if data[0]['count'] != 0:
            # [i] Adding entry to the active_event list in realtime (each iteration)
            # if user adds or exists in the database
            for entry in data[0]['data']:
                if entry not in active_event:
                    active_event.append(entry)

            # [i] Removing entry to the active_event list in realtime (each iteration)
            # if user removes or deleted from the database on expiry
            for entry in active_event:
                if entry not in data[0]['data']:
                    active_event.remove(entry)

            for entry in active_event:
                if entry not in active_entry:
                    Thread(target=core_engine, args=(entry, )).start()
                    active_entry.append(entry)
                    print(f"Starting thread '{entry['title']}' {datetime.now().time()}...")

        sleep(1)


# [i] Accessing the data & time to remind the user in time
def core_engine(entry):
    while True:
        print(f"Running core_engine '{entry['title']}' {datetime.now().time()}...")
        data_update_(method='PULL')
        # [i] Collecting the data
        data = data_type_(1)

        # [i] Entry deletion from database on user request
        if entry not in active_event:
            active_entry.remove(entry)
            return None

        # [i] Entry deletion from database on expiry
        if entry['repeat']:
            if entry['loop']['end_date']:
                if entry['loop']['end_date'] == datetime.now().date():
                    if entry['when']['time'] < datetime.now().time():
                        del_data(1, data[0]['data'].index(entry), _prompt=False)
        else:
            if entry['when']['date'] == datetime.now().date():
                if entry['when']['time'] <= datetime.now().time():
                    notify_desktop(title=entry['title'], message=entry['description'])
                    active_entry.remove(entry)
                    print(f"Stopping thread {entry['title']}...")
                    del_data(1, data[0]['data'].index(entry), _prompt=False)
                    return None

        sleep(1)


def notify_desktop(title: str = "Title", message: str = "Here the brief message goes."):
    notification.notify(
        title=title.upper(),
        message=message,
        timeout=5,
        ticker="Hi",
        toast=True
    )


Thread(target=prt).start()
Thread(target=event_engine).start()
