from collections import UserDict


class AddressBook(UserDict):

    def add_record(self, record):
        key = record.name.value
        self.data[key] = record


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phone_numbers = []

    def add_phone_number(self, phone_number):
        self.phone_numbers.append(phone_number)

    def delete_phone_number(self, phone_number):
        if phone_number in self.phone_numbers:
            self.phone_numbers.remove(phone_number)

    def edit_phone_number(self, old_phone_number, new_phone_number):
        if old_phone_number in self.phone_numbers:
            index = self.phone_numbers.index(old_phone_number)
            self.phone_numbers[index] = new_phone_number


class Field:

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Name(Field):

    def __init__(self, name):
        super().__init__('Name', name)


class Phone(Field):

    def __init__(self, phone_number):
        super().__init__('Phone_number', phone_number)


address_book = AddressBook()

record_abonent_1 = Record('Anna Vlasiuk')
record_abonent_1.add_phone_number(Phone('+38096569812'))
record_abonent_1.add_phone_number(Phone('+38096145873'))
address_book.add_record(record_abonent_1)

record_abonent_2 = Record('Nikola Smagliuk')
record_abonent_2.add_phone_number(Phone('+380636598745'))
record_abonent_2.add_phone_number(Phone('+380501431564'))
address_book.add_record(record_abonent_2)

record_abonent_1.edit_phone_number(Phone('+38096569812'), Phone('0965865952'))
record_abonent_2.edit_phone_number(Phone('+380636598745'), Phone('0501503625'))

for name, phone in address_book.data.items():
    print(f"{name}: {phone}")
