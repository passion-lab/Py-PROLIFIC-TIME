# [i] Notification Handler
# from main import *
# from EventData import *
# from Engine import *
from plyer import notification


msg = """Python is one of the most accessible programming languages available because of Its simplified syntax that 
gives emphasis on natural language. It is highly used in machine learning and data science applications which are 
some of the biggest trend. """


def notify_desktop(title: str = "Title", message: str = "Here the brief message goes."):
    notification.notify(
        title=title.upper(),
        message=msg,
        # app_name="PT",
        app_icon="./Icons/countdown.ico",
        timeout=5,
        # ticker="PT",
        # toast=False
    )


notify_desktop("Hello", "This is a message")
