import argparse
import json
import signal
import sys


contacts_file_name = None
contacts = {}


def system_signal_handler(sig, frame):
    _, _ = sig, frame
    print("\nTermination signal received. Shutting down...")
    before_exit()
    sys.exit(0)


def load_contacts():
    global contacts
    with open(contacts_file_name, "r") as fh:
        contacts = json.load(fh)

def save_contacts():
    with open(contacts_file_name, "w") as fh:
        json.dump(contacts, fh, indent=4)


def greet():
    print('How can I help you?')


def add_contact(name: str, phone: str):
    if name in contacts:
        return f"Name {name} already exists. Use command \"change\" to update"
    
    contacts[name] = phone
    return f"{name} was added to your contacts"


def change_contact():
    pass


def show_phone():
    pass


def show_all():
    pass


def before_exit():
    save_contacts()


def on_startup():
    load_contacts()


def command_handler(command: dict):
    cmd = command['command']
    
    if cmd == 'exit':
        print("Shutting down...")
        before_exit()
        sys.exit(0)
    elif cmd == "hello":
        return greet()
    elif cmd == "add":
        return add_contact(command['name'], command['phone'])
    else:
        return f'Unknown command {cmd}. Try again'


def command_parser(user_input: str):
    if user_input == '':
        return None
    
    command_components = user_input.split()
    command = command_components[0]
    name = ''
    phone = ''

    if len(command_components) > 1:
        name = command_components[1]

    if len(command_components) > 2:
        phone = command_components[2]

    return {'command': command, 'name': name, 'phone': phone}


def run():
    while True:
        user_input = input("console bot >>> ")
        command = command_parser(user_input)
        if command is None:
            print('No command was entered. Try again')
        message = command_handler(command)
        if message:
            print(message)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, system_signal_handler)
    signal.signal(signal.SIGTERM, system_signal_handler)
    signal.signal(signal.SIGBREAK, system_signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str,
                        help='Path to the csv file with users data',
                        default='./data/contacts.json')

    args = parser.parse_args()
    contacts_file_name = args.file

    on_startup()

    run()
