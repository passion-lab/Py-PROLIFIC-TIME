# [i] Notification Handler
# from main import *
# from EventData import *
# from Engine import *
from plyer import notification


def notify_desktop(title: str = "Title", message: str = "Here the brief message goes."):
    notification.notify(
        title=title.upper(),
        message=message,
        timeout=5,
        ticker="Hi",
        toast=True
    )

