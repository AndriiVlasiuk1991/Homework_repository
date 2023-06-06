phonebook = {}


class CopyKeyError(Exception):
    pass


def input_error(func):
    def inner(name, phone_number):
        try:
            func(name, phone_number)
        except KeyError:
            print(f"Контакт {name} не знайдений\n")
        except ValueError:
            print(f"Номер телефону може складатися лише з цифр.\n")
        except CopyKeyError:
            print(f"Контакт {name} вже був доданий.\n")

    return inner


def main():
    action = input(f'Введіть команду "hello" для початку роботи з ботом:\n')
    if action.lower() == "hello":
        print("Вітаю! Чим я можу Вам допомогти?\n")
        while True:
            action = input(
                f"""Введіть одну з запропонованих команд:\n
                - "add ..." - бот додасть нове ім'я та номер телефону в телефонну книгу (введить ім'я та номер телефону, обов'язково через пробіл)\n
                - "change ..." - бот додасть новий номер телефону до існуючого імені в телефонну книгу (введить ім'я та номер телефону, обов'язково через пробіл)\n 
                - "phone ..." - бот виведе у консоль номер телефону для зазначеного імені контакту\n 
                - "show all" - бот виводить всі збереженні контакти з номерами телефонів\n 
                - "good bye", "close", "exit" - бот завершує свою роботу\n\n"""
            )

            if action.lower().split(" ")[0] == "add":
                add_contact(
                    name=action.split(" ")[1], phone_number=action.split(" ")[2]
                )
            elif action.lower().split(" ")[0] == "change":
                update_contact(
                    name=action.split(" ")[1], phone_number=action.split(" ")[2]
                )
            elif action.lower().split(" ")[0] == "phone":
                get_phone(name=action.split(" ")[1], phone_number="")
            elif action.lower() == "show all":
                get_all_contact()
            elif action.lower() in ["good bye", "close", "exit"]:
                print("До побачення!\n")
                break
            else:
                print("Введена невірна команда, спробуйте ще раз.\n")
    else:
        print("Введена невірна команда, спробуйте ще раз.\n")


@input_error
def add_contact(name, phone_number):
    if name in phonebook:
        raise CopyKeyError()
    else:
        phonebook.update({name: int(phone_number)})
        print(f"Додано контакт: {name} - {phone_number}\n")


@input_error
def update_contact(name, phone_number):
    if name in phonebook:
        phonebook.update({name: phone_number})
        print(f"Номер телефону оновлено: {name} - {phonebook[name]}\n")
    else:
        raise KeyError


@input_error
def get_phone(name, phone_number):
    print(f"Номер телефону контака {name} - {phonebook[name]}\n")


def get_all_contact():
    print(f"Всі контакти:\n")
    for key, value in phonebook.items():
        print(f"\t{key} - {value}\n")


if __name__ == "__main__":
    main()
