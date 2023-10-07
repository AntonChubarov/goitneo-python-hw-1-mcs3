import signal
import sys
import time


contacts = {}


def system_signal_handler(sig, frame):
    _, _ = sig, frame
    # TODO Perform cleanup operations here
    print("Shutting down gracefully...")
    sys.exit(0)


def load_contacts():
    pass


def greet():
    print('How can I help you?')


def add_contact():
    pass


def change_contact():
    pass


def show_phone():
    pass


def show_all():
    pass


def before_exit():
    pass


def command_parser():
    pass


def command_handler():
    pass


def run():
    print('bot ran')
    while True:
        time.sleep(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, system_signal_handler)
    signal.signal(signal.SIGTERM, system_signal_handler)
    signal.signal(signal.SIGBREAK, system_signal_handler)
    run()
