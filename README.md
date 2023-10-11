# Colleagues' Birthday Assistant
This tool helps you identify which colleagues have birthdays coming up within
the next week.

To run the Colleagues' Birthday Assistant, navigate to the
'goitneo-python-hw-1-mcs3' folder and execute the following command:
```console
python3 birthday_assistant.py --file ./data/users.csv
```
Make sure the specified CSV file contains two columns: "name," which holds the
full name of the user, and "birthday," which stores the user's birth date in
the "YYYY-MM-DD" format.

Alternatively, you can run the application with the default file as follows:
```console
python3 birthday_assistant.py
```
In this case, the tool will use the default './data/users.csv' file.

# Console bot
Console Bot is a command-line interface application for managing, updating, and
viewing phone numbers. The app saves the current list of contacts to a file at
the end of each session.

To run the Console Bot, go to the 'goitneo-python-hw-1-mcs3' folder and execute
the following command:
```console
python3 console_bot.py --file ./data/contacts.json
```
Ensure that the specified JSON file is formatted as a dictionary, where keys
represent names, and values are phone numbers (strings).

You can also run the application with the default file as follows:
```console
python3 console_bot.py
```
In this case, the tool will use the default './data/contacts.json' file.
