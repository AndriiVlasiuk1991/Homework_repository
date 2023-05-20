from datetime import datetime, timedelta

days_name = {
    0: "Понеділок",
    1: "Вівторок",
    2: "Середа",
    3: "Четвер",
    4: "П'ятниця",
    5: "Субота",
    6: "Неділя",
}

list_days = {
    "Понеділок": [],
    "Вівторок": [],
    "Середа": [],
    "Четвер": [],
    "П'ятниця": [],
    "Субота": [],
    "Неділя": [],
}


def get_birthdays_per_week(list_of_people):
    actual_date = datetime.now()
    interval = actual_date + timedelta(days=7)

    for people in list_of_people:
        full_name = " ".join(people.split()[0:2])
        birthday = datetime.strptime(people.split()[2], "%d.%m.%Y")

        if actual_date.day <= birthday.day <= interval.day:
            congrat_day = actual_date + timedelta(days=(birthday.day - actual_date.day))

            for day_num, day_name in days_name.items():
                if congrat_day.weekday() in [5, 6]:
                    day_of_congrat = 0
                else:
                    day_of_congrat = congrat_day.weekday()

                if day_num is day_of_congrat:
                    for day in list_days.keys():
                        if day_name == day:
                            list_days.get(day).append(full_name)

    # Виводимо дні починаючи з поточного
    for day_num, day_name in days_name.items():
        if day_num in range(actual_date.weekday(), 7):
            for day, name_list in list_days.items():
                if day == day_name and name_list:
                    list = ", ".join(name_list[:])
                    print(f"{day}: {list}")

    for day_num, day_name in days_name.items():
        if day_num in range(0, actual_date.weekday()):
            for day, name_list in list_days.items():
                if day == day_name and name_list:
                    list = ", ".join(name_list[:])
                    print(f"{day}: {list}")


def main():
    list_of_people = [
        "Дарья Тютерева 21.05.1991",
        "Вероника Томенко 20.05.2000",
        "Наташа Шевченко 26.06.1980",
        "Дмитрий Демяненко 24.05.1995",
        "Валерия Самошина 30.12.2002",
        "Виталий Ткачук 28.5.1998",
        "Елена Жукова 04.07.2001",
        "Марина Гриб 30.05.2009",
        "Юлия Бугай 18.02.1987",
        "Андрей Тарасюк 26.05.2002",
    ]

    get_birthdays_per_week(list_of_people)


if __name__ == "__main__":
    main()
