from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone(value)

    def validate_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone must be a 10-digit number.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

address_book = AddressBook()
