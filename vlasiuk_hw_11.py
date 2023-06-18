from collections import UserDict
from collections.abc import Iterator
from datetime import date


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        if not isinstance(value, date):
            raise ValueError("Неправильне значення дати")
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, date):
            raise ValueError("Неправильне значення дати")
        self._value = new_value


class Phone(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.isdigit():
            raise ValueError("Неправильне значення номера телефону")
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, str) or not new_value.isdigit():
            raise ValueError("Неправильне значення номера телефону")
        self._value = new_value


class Record:
    def __init__(self, name: Name, phone: Phone, birthday: Birthday = None):
        self.name = name
        if phone:
            self.phones = []
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone_number(self, phone_number):
        self.phones.append(phone_number)

    def delete_phone_number(self, phone_number):
        if phone_number in self.phones:
            self.phones.remove(phone_number)

    def edit_phone_number(self, old_phone_number, new_phone_number):
        if old_phone_number in self.phones:
            index = self.phones.index(old_phone_number)
            self.phones[index] = new_phone_number

    def days_to_birthday(self):
        if self.birthday is None:
            return None
        today = date.today()
        next_birthday = date(
            today.year, self.birthday.value.month, self.birthday.value.day
        )
        if next_birthday < today:
            next_birthday = date(
                today.year + 1, self.birthday.value.month, self.birthday.value.day
            )
        days_left = (next_birthday - today).days
        return days_left

    def __str__(self):
        phone_numbers = ", ".join([phone.value for phone in self.phones])
        if self.birthday:
            return f"Name: {self.name.value}, Phones: {phone_numbers}, Birthday: {self.birthday.value}"
        else:
            return f"Name: {self.name.value}, Phones: {phone_numbers}"


class AddressBook(UserDict):
    def add_record(self, record):
        key = record.name.value
        self.data[key] = record

    def __iter__(self):
        self.keys_iterator = iter(self.data.keys())
        return self

    def __next__(self):
        key = next(self.keys_iterator)
        return self.data[key]


if __name__ == "__main__":
    address_book = AddressBook()

    name_1 = Name("Bill")
    phone_1 = Phone("0501603965")
    birthday_1 = Birthday(date(1991, 5, 7))
    rec = Record(name_1, phone_1, birthday_1)
    rec.edit_phone_number(phone_1, Phone("0661532698"))
    address_book.add_record(rec)

    name_2 = Name("Ann")
    phone_2 = Phone("0965663265")
    birthday_2 = Birthday(date(1993, 4, 6))
    rec = Record(name_2, phone_2, birthday_2)
    rec.edit_phone_number(phone_2, Phone("0671515478"))
    address_book.add_record(rec)

    assert isinstance(address_book["Bill"], Record)
    assert isinstance(address_book["Bill"].name, Name)
    assert isinstance(address_book["Bill"].phones, list)
    assert isinstance(address_book["Bill"].phones[0], Phone)
    assert address_book["Bill"].phones[0].value == "0661532698"

    assert isinstance(address_book["Ann"], Record)
    assert isinstance(address_book["Ann"].name, Name)
    assert isinstance(address_book["Ann"].phones, list)
    assert isinstance(address_book["Ann"].phones[0], Phone)
    assert address_book["Ann"].phones[0].value == "0671515478"

    print("All Ok)")

    # Виведення записів посторінково
    page_size = 1  # Вказати кількість рядків на сторінці
    page_number = 1  # Вказати номер сторінки
    records_iter = iter(address_book)
    total_records = len(address_book)
    start_index = (page_number - 1) * page_size
    end_index = page_number * page_size

    while start_index < total_records:
        records_on_page = list(records_iter)[start_index:end_index]
        for record in records_on_page:
            print(record)

        start_index = end_index
        end_index = start_index + page_size
