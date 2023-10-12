"""
This module contains get_birthdays_per_week function which selects users
that should be congratulated this week from the list of dictionaries that
contains two keys: "name" and "birthday" where "birthday" is in the format
"YYYY-MM-DD".

Author: Anton Chubarov
Date: October 11, 2023
"""

import argparse
import csv
import datetime
import sys


EXPECTED_COLUMNS = ["name", "birthday"]


def load_users_from_csv_file(path: str) -> list[dict[str, datetime.date]]:
    """
    Load users data from a CSV file and convert it into a list of dictionaries.

    Args:
        path (str): The path to the CSV file containing user data. The CSV file
        should have two columns, "name" and "birthday", where "birthday" is in
        the format "YYYY-MM-DD".

    Returns:
        list of dict: A list of dictionaries, where each dictionary represents
        a user. Each user dictionary has two keys: "name" (str) and "birthday"
        (datetime.date).

    Raises:
        FileNotFoundError: If the specified file at "path" does not exist.
        csv.Error: If there is an issue with reading the CSV file.
        ValueError: If the "birthday" column in the CSV file is not in the
        correct format, or CSV file hasn't required fields.

    Example:
        If the CSV file at "path" contains the following data:
        name,birthday
        Alice Smith,1990-05-15
        Bob Jones,1985-12-10

        Calling load_users_from_file(path) will return:
        [{"name": "Alice Smith", "birthday": datetime.date(1990, 5, 15)},
         {"name": "Bob Jones", "birthday": datetime.date(1985, 12, 10)}]
    """

    users: list[dict[str, datetime.date]] = []

    if not path.endswith(".csv"):
        raise csv.Error(f"{path} is not a CSV file")

    with open(path, "r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh)
        if not set(EXPECTED_COLUMNS).issubset(set(csv_reader.fieldnames)):
            raise csv.Error(f"file {path} does not have the expected columns"
                            " \"name\" and \"birthday\"")
        row_number = 1
        for row in csv_reader:
            row_number += 1
            try:
                row["birthday"] = datetime.datetime.strptime(
                    row["birthday"], "%Y-%m-%d")
            except ValueError as e:
                print(f"Skipping row {row_number} {row}: {e}")
                continue
            users.append(row)

    return users


def get_birthdays_per_week(
        users: list[dict[str, datetime.date]]) -> dict[str, list[str]]:
    """
    Print a list of users whose birthdays are coming up in the current week.

    Args:
        users (list of dict): A list of user dictionaries. Each dictionary
        should have two keys: "name" (str) and "birthday" (datetime.date).

    Returns:
        dayly_sorted_users_to_congratulate (dict of lists of strings): a dict
        with keys that represents days of upcoming week where values is a lists
        of users with upcoming birthdays for each day of the week.

    Example:
        If the "users" list contains user data like this and today is
        2023-10-07:
        [{"name": "Alice Smith", "birthday": datetime.date(1990, 10, 7)},
        {"name": "Bob Jones", "birthday": datetime.date(1985, 10, 9)},
        {"name": "Charlie Walker", "birthday": datetime.date(1995, 10, 10)}]

        Calling get_birthdays_per_week(users) will return:
        {"Monday": ["Alice Smith", "Bob Jones"], "Tuesday": ["Charlie Walker"]}
    """
    today = datetime.datetime.today().date()

    users_to_congratulate: dict[str, list[str]] = {}

    for user in users:
        birthday_this_year = user["birthday"].date().replace(year=today.year)

        days_to_period_start, days_to_period_end = 0, 7
        if today.strftime("%A") == "Monday":
            days_to_period_start, days_to_period_end = -2, 5
        elif today.strftime("%A") == "Sunday":
            days_to_period_start, days_to_period_end = -1, 6

        delta_days = (birthday_this_year - today).days

        if days_to_period_start <= delta_days < days_to_period_end:
            day_name = birthday_this_year.strftime("%A")

            if day_name in ("Saturday", "Sunday"):
                day_name = "Monday"

            if day_name not in users_to_congratulate:
                users_to_congratulate[day_name] = []

            users_to_congratulate[day_name].append(user["name"])

    birthday_days = list(users_to_congratulate.keys())
    sorted_days = [(datetime.datetime.today()+datetime.timedelta(days=i)).
                   strftime("%A") for i in range(7)]
    sorted_days = list(filter(
        lambda day: day in birthday_days, sorted_days))

    dayly_sorted_users_to_congratulate: dict[str, list] = {}

    for day in sorted_days:
        names = ", ".join(users_to_congratulate[day])
        dayly_sorted_users_to_congratulate[day] = names

    return dayly_sorted_users_to_congratulate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str,
                        help="""path to the csv file with users data. When not
                        specified ./data/users.csv will be used""",
                        default="./data/users.csv"
                        )

    args = parser.parse_args()

    path = args.file

    try:
        users = load_users_from_csv_file(path)
    except FileNotFoundError:
        print(f"File {path} not found")
        sys.exit(0)
    except csv.Error as csve:
        print(f"CSV error: {csve}")
        sys.exit(0)
    except ValueError as ve:
        print(f"CSV structure validation failed: {ve}")
        sys.exit(0)

    users_to_congratulate = get_birthdays_per_week(users)

    for name, users in users_to_congratulate.items():
        print(f"{name}: {users}")


if __name__ == "__main__":
    main()
