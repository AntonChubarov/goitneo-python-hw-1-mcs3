"""
This module contains get_birthdays_per_week function which selects your
coleagues that should be congratulated this week.

Author: Anton Chubarov
Date: October 10, 2023
"""

import argparse
import csv
import datetime


EXPECTED_COLUMNS = ['name', 'birthday']


def load_users_from_file(path: str) -> list[dict[str, datetime.date]]:
    """
    Load user data from a CSV file and convert it into a list of dictionaries.

    Args:
        path (str): The path to the CSV file containing user data. The CSV file
                    should have two columns, "name" and "birthday," where
                    "birthday" is in the format 'YYYY-MM-DD'.

    Returns:
        list of dict: A list of dictionaries, where each dictionary represents
                      a user. Each user dictionary has two keys: 'name' (str)
                      and 'birthday' (datetime.date).

    Raises:
        FileNotFoundError: If the specified file at 'path' does not exist.
        csv.Error: If there is an issue with reading the CSV file.
        ValueError: If the 'birthday' column in the CSV file is not in the
        correct format, or CSV file hasn't required fields.

    Example:
        If the CSV file at 'path' contains the following data:
        name,birthday
        Alice Smith,1990-05-15
        Bob Jones,1985-12-10

        Calling load_users_from_file(path) will return:
        [{'name': 'Alice Smith', 'birthday': datetime.date(1990, 5, 15)},
         {'name': 'Bob Jones', 'birthday': datetime.date(1985, 12, 10)}]
    """

    users = []

    if not path.endswith('.csv'):
        print(f"{path} is not a CSV file")
        return users

    try:
        with open(path, 'r', encoding='utf-8') as fh:
            csv_reader = csv.DictReader(fh)

            if not set(EXPECTED_COLUMNS).issubset(set(csv_reader.fieldnames)):
                raise ValueError(f"""file {path} does not have the expected
                                 columns \"name\" and \"birthday\"""")

            row_number = 0

            for row in csv_reader:
                row_number += 1

                try:
                    row['birthday'] = datetime.datetime.strptime(
                        row['birthday'], '%Y-%m-%d')
                except ValueError as e:
                    print(f"Skipping row {row_number} {row}: {e}")
                    continue

                users.append(row)

    except FileNotFoundError:
        print(f"File {path} not found")
    except csv.Error as e:
        print(f"CSV error: {e}")
    except ValueError as ve:
        print(f"CSV structure validation failed: {ve}")

    return users


def get_birthdays_per_week(users: list[dict[str, datetime.date]]):
    """
    Print a list of users whose birthdays are coming up in the current week.

    Args:
        users (list of dict): A list of user dictionaries. Each dictionary
                              should have two keys: 'name' (str) and 'birthday'
                              (datetime.date).

    Prints:
        None: This function prints a list of users with upcoming birthdays for
              each day of the current week.

    Example:
        If the 'users' list contains user data like this and today is
        2023-10-07:
        [{'name': 'Alice Smith', 'birthday': datetime.date(1990, 10, 7)},
         {'name': 'Bob Jones', 'birthday': datetime.date(1985, 10, 9)},
         {'name': 'Charlie Walke', 'birthday': datetime.date(1995, 10, 10)}]

        Calling get_birthdays_per_week(users) will print:
        Monday: Alice, Bob
        Tuesday: Charlie
    """
    today = datetime.datetime.today().date()

    users_to_congratulate: dict[str, list] = {}

    for user in users:
        name = user['name']
        birthday = user['birthday'].date()
        birthday_this_year = birthday.replace(year=today.year)

        delta_days = (birthday_this_year - today).days

        days_to_period_start, days_to_period_end = 0, 7
        if today.strftime('%A') == 'Monday':
            days_to_period_start, days_to_period_end = -2, 5
        elif today.strftime('%A') == 'Sunday':
            days_to_period_start, days_to_period_end = -1, 6

        if days_to_period_start <= delta_days < days_to_period_end:
            day_name = birthday_this_year.strftime('%A')

            if day_name in ('Saturday', 'Sunday'):
                day_name = 'Monday'

            if day_name not in users_to_congratulate:
                users_to_congratulate[day_name] = []

            users_to_congratulate[day_name].append(name)

    birthday_days = list(users_to_congratulate.keys())
    sorted_days = [(datetime.datetime.today()+datetime.timedelta(days=i)).
                   strftime('%A') for i in range(7)]
    sorted_days = list(filter(
        lambda day: day in birthday_days, sorted_days))

    dayly_sorted_users_to_congratulate: dict[str, list] = {}

    for day in sorted_days:
        names = ', '.join(users_to_congratulate[day])
        dayly_sorted_users_to_congratulate[day] = names

    return dayly_sorted_users_to_congratulate


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str,
                        help="""path to the csv file with users data. When not
                        specified ./data/users.csv will be used""",
                        default='./data/users.csv'
                        )

    args = parser.parse_args()

    users = load_users_from_file(args.file)

    users_to_congratulate = get_birthdays_per_week(users)
    for name, users in users_to_congratulate.items():
        print(f'{name}: {users}')
