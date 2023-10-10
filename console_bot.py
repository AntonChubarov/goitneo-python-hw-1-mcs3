import argparse
import json
import signal
import sys


contacts_file_name: str = None
contacts = {}


def handle_system_signal(sig, frame):
    _, _ = sig, frame
    print("\nTermination signal received. Shutting down...")
    shutdown()


def load_contacts():
    if not contacts_file_name.endswith('.json'):
        raise ValueError(f"file {contacts_file_name} is not a JSON file")
    
    global contacts
    with open(contacts_file_name, "a+") as fh:
        contacts = json.load(fh)


def save_contacts():
    if len(contacts) == 0:
        return
    
    with open(contacts_file_name, "w") as fh:
        json.dump(contacts, fh, indent=4)


def greet() -> str:
    return 'How can I help you?'


def add_contact(name: str, phone: str) -> str:
    if name in contacts:
        return f"Name {name} already exists. Use command \"change\" to update"

    contacts[name] = phone
    return f"{name} was added to your contacts"


def change_contact(name: str, phone: str) -> str:
    if name not in contacts:
        return f"There is no {name} in contacts. Use command \"add\" to create"

    contacts[name] = phone
    return f"{name}'s contact was updated"


def show_phone(name: str) -> str:
    if name not in contacts:
        return f"There is no {name} in contacts. Use command \"add\" to create"
    
    return contacts[name]


def show_all() -> str:
    if len(contacts) == 0:
        return "You have no saved contacts yet"
    
    contacts_to_print = ""

    for name, phone in contacts.items():
        contacts_to_print += name + " " + phone + "\n"

    return contacts_to_print


def shutdown():
    save_contacts()
    sys.exit(0)


def init():
    signal.signal(signal.SIGINT, handle_system_signal)
    signal.signal(signal.SIGTERM, handle_system_signal)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str,
                        help='Path to the csv file with users data',
                        default='./data/contacts.json')

    args = parser.parse_args()

    global contacts_file_name
    contacts_file_name = args.file

    load_contacts()


def handle_command(command: dict) -> str:
    cmd = command['command']

    if cmd == "hello":
        return greet()
    elif cmd == "add":
        return add_contact(command['name'], command['phone'])
    elif cmd == "change":
        return change_contact(command['name'], command['phone'])
    elif cmd == "phone":
        return show_phone(command['name'])
    elif cmd == "all":
        return show_all()
    else:
        return f'Invalid command: {cmd}'


def parse_command(user_input: str) -> dict[str, str]:
    if user_input == '':
        return None

    command_components = user_input.split()
    command = command_components[0].lower()
    name = ''
    phone = ''

    if len(command_components) > 1:
        name = command_components[1]

    if len(command_components) > 2:
        phone = command_components[2]

    return {'command': command, 'name': name, 'phone': phone}


def main():
    while True:
        user_input = input("console bot >>> ")
        command = parse_command(user_input)
        if command is None:
            print('No command was entered. Try again')
        elif command['command'] in ('exit', 'q', 'quit', 'close'):
            break
        message = handle_command(command)
        if message:
            print(message)

    print("Good bye!")
    shutdown()


if __name__ == '__main__':
    init()
    main()
