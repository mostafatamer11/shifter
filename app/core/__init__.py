import datetime
import pandas as pd


def isleap(Year):
    if((Year % 400 == 0) or \
        (Year % 100 != 0) and \
        (Year % 4 == 0)):
        return True
    else:
        return False

my_date = datetime.date.today()
year, week_num, day_of_week = my_date.isocalendar()
month = my_date.month + 1 if my_date.month < 12 else 1

DAYS = ["monday", "tuesday", "wensday", "thursday", "friday", "saturday", "sunday"]
MONTHS = {"jan": 31, "feb": isleap(year) + 28, "mar": 31,
          "april": 30, "may": 31, "june": 30,
          "july": 31, "aug": 31, "sep": 30,
          "oct": 31, "nov": 30, "dec": 31}

def generate(vications:dict[str, list[tuple] | None], month_i:str | None):
    global month
    next_month = MONTHS[list(MONTHS.keys())[(month - 1)]]
    shifts_no = MONTHS[month_i] if month_i else next_month
    month = month_i if month_i else month
    shifts = []

    for i in range(shifts_no):
        a = []
        for name in vications:
            free = vications[name]

            if not free:
                a.append(name)

            else:
                is_free = False
                for t in free:
                    if (i >= t[0] and i <= t[1]) or (i >= t[0] and i <= t[1]):
                        is_free = True

                if not is_free:
                    a.append(name)

        temp = []
        flag = False
        if not(all(element in shifts for element in a)):
            for a_name in a:
                if not a_name in shifts:
                    shifts.append(a_name)
                    flag = True
                    break

        if flag: continue

        for a_name in a:
            if not a_name in shifts:
                shifts.append(a_name)
                break

            else:
                reversed_lst = shifts[::-1]  # Reverse the list
                last_index = len(shifts) - reversed_lst.index(a_name) - 1
                temp.append(last_index)

        if temp:
            shifts.append(shifts[min(temp)])

    return shifts


def file_gen(shifts, filepath):
    global year, month
    year += 1 if month == 1 else 0
    new_date = datetime.date(year, month, 1)
    weekday = new_date.weekday()
    weekdays = [DAYS[(weekday + i) % 7] for i in range(len(shifts))]
    dates = [datetime.date(year, month, 1 + i).strftime("%d/%m/%Y") for i in range(len(shifts))]
    df = pd.DataFrame()
    df["name"] = shifts
    df["shift"] = ["from 8:00 A.M GMT+2(cairo) to 8:00 P.M GMT+2(cairo)" if i%2 == 0 else "from 8:00 P.M GMT+2(cairo) to 8:00 A.M GMT+2(cairo)" for i, _ in enumerate(shifts)]
    df["weekday"] = weekdays
    df["date"] = dates
    df.to_csv(filepath, index=False)

