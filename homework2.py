from collections import UserDict

class Field:
    # клас Field є базовим для полів
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        # додати необхідну логіку для перевірки правильності введеного імені

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone(value)
    
    def validate_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Invalid phone number format. Please enter a 10-digit number.")
        # логіка для перевірки правильності формату номера телефону
    

class Record:
    # клас представляє запис в адресній книзі
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        # логіка для додавання номера телефону до запису

    def delete_phone(self, phone):
        for i in range(len(self.phones)):
            if self.phones[i].phone == phone:
                del self.phones[i]
                break
        # логіка для видалення номера телефону з запису

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        # логіка для редагування номера телефону в записі

    def search_phone(self, phone):
        return phone in self.phones
        # логіка для пошуку номера телефону в записі

class AddressBook(UserDict):
    # клас представляє адресну книгу, яка є словником записів
    def add_record(self, record):
        self.data[record.name.value] = record
        # логіка для додавання запису до адресної книги

    def search_record(self, name):
        return self.data.get(name)
        # логіка для пошуку запису за ім'ям в адресній книзі

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
        # логіка для видалення запису за ім'ям з адресної книги


def input_error(func):
    # цей декоратор обробляє помилки, які виникають у функціях введення користувача
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command syntax."

    return inner

@input_error
def add_contact(args, contacts):         
    # Функція для додавання нового контакту до словника contacts.
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):     
    # Функція для зміни інформації про існуючий контакт у словнику contacts.
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(args, contacts):     
    # Функція для відображення номера телефону вказаного контакту.
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        raise KeyError("Contact not found.")

def parse_input(user_input):        
    # Ця функція розбирає введену користувачем команду на команду (перший елемент) та аргументи (решта елементів).
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def show_all(contacts):             
    # Функція для відображення всіх контактів у словнику contacts.
    if contacts:
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    else:
        print("No contacts saved.")

def main():                         
    # Головна функція програми, яка запускається при старті.
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
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
