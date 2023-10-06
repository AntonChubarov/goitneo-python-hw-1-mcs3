import argparse
import csv
import datetime


def load_users_from_file(path):
    with open(path, 'r') as fh:
        csv_reader = csv.DictReader(fh)
        data = []
    
        for row in csv_reader:
            row['birthday'] = datetime.datetime.strptime(row['birthday'], "%Y-%m-%d")
            
            data.append(row)

    return data


def get_birthdays_per_week(users):
    today = datetime.datetime.today().date()

    users_to_congratulate = {}

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if delta_days < 7:
            day_name = birthday_this_year.strftime("%A")

            if day_name in ('Saturday', 'Sunday'):
                day_name = 'Monday'

            if day_name not in users_to_congratulate:
                users_to_congratulate[day_name] = []

            users_to_congratulate[day_name].append(name)

    for day, names in users_to_congratulate.items():
        print('{day}: {names}'.format(day=day, names=', '.join(names)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='Path to the csv file with users data', default='./data/users.csv')
    
    args = parser.parse_args()

    users = load_users_from_file(args.file)

    get_birthdays_per_week(users)
