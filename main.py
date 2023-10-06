import argparse
import csv
import datetime


days_in_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


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

    birthday_days = list(users_to_congratulate.keys())
    current_day_name = today.strftime("%A")
    current_day_order_index = days_in_order.index(current_day_name)
    sorted_days = days_in_order[current_day_order_index:] + days_in_order[:current_day_order_index]
    sorted_days = list(filter(lambda day: day in birthday_days, sorted_days))

    for day in sorted_days:
        print('{day}: {names}'.format(day=day, names=', '.join(users_to_congratulate[day])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='Path to the csv file with users data', default='./data/users.csv')
    
    args = parser.parse_args()

    users = load_users_from_file(args.file)

    get_birthdays_per_week(users)
