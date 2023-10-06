import csv


def load_users_from_file(path):
    with open(path, 'r') as fh:
        csv_reader = csv.DictReader(fh)
        data = []
    
        for row in csv_reader:
            data.append(row)

    return data


def get_birthdays_per_week(users):
    pass


if __name__ == '__main__':
    users = load_users_from_file('./data/users.csv')

    print(users)

    get_birthdays_per_week(users)
