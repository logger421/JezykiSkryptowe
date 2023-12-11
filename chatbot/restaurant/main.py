# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime

def convert_time_to_int(time_str):
    # Check if the time is in 12-hour format (contains AM or PM)
    if 'AM' in time_str or 'PM' in time_str:
        # Parse 12-hour format
        parsed_time = datetime.strptime(time_str, '%I:%M%p')
    else:
        # Parse 24-hour format
        parsed_time = datetime.strptime(time_str, '%H:%M')

    return parsed_time.hour

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time = convert_time_to_int("6:30PM")
    print(time)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
