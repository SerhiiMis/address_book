import json
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone(value)
    
    def validate_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Invalid phone number format. Please enter a 10-digit number.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                del self.phones[i]
                break

    def edit_phone(self, old_phone, new_phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def search_phone(self, phone):
        return any(p.value == phone for p in self.phones)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_record(self, name):
        return name in self.data

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."
    return inner

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return f"Contact {name} with phone number {phone} has been added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact information has been updated."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        raise KeyError("Contact not found.")

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def show_all(contacts):
    if contacts:
        for name, phone in contacts.items():
            print(f"Name: {name}, Phone: {phone}")
    else:
        print("No contacts found.")

def save_to_file(filename, address_book):
    with open(filename, "w") as file:
        data = {
            name: {
                "phones": [phone.value for phone in record.phones]
            } for name, record in address_book.items()
        }
        json.dump(data, file, indent=4)
        print(f"Contacts saved to {filename}.")

def load_from_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)  # Try loading JSON data
            address_book = AddressBook()
            for name, record_data in data.items():
                record = Record(name)
                for phone in record_data["phones"]:
                    record.add_phone(phone)
                address_book.add_record(record)
            print(f"Contacts loaded from {filename}.")
            return address_book
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty address book.")
        return AddressBook()  # Return an empty address book if file is missing
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {filename}. The file may be corrupted or empty.")
        # Optionally, you can create a new file if corrupted:
        open(filename, 'w').close()  # Create a new empty file
        return AddressBook()  # Return an empty address book


def main():
    filename = "contacts.json"
    contacts = load_from_file(filename)
    
    print("Welcome to the phonebook!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_to_file(filename, contacts)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            show_all(contacts)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
