from flask import Flask, request, jsonify, render_template
from collections import UserDict
import json

app = Flask(__name__)

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

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_record(self, name):
        return name in self.data

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

address_book = AddressBook()

# Load contacts from file
def load_from_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for name, record_data in data.items():
                record = Record(name)
                for phone in record_data["phones"]:
                    record.add_phone(phone)
                address_book.add_record(record)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass

# Save contacts to file
def save_to_file(filename):
    with open(filename, "w") as file:
        data = {
            name: {"phones": [phone.value for phone in record.phones]}
            for name, record in address_book.items()
        }
        json.dump(data, file, indent=4)

# Load contacts when the app starts
load_from_file("contacts.json")

@app.route('/')
def index():
    return render_template('index.html', contacts=address_book)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    if name and phone:
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        save_to_file("contacts.json")
        return jsonify({"message": f"Contact {name} added successfully!"})
    return jsonify({"error": "Name and phone are required!"})

@app.route('/contacts')
def get_contacts():
    contacts_list = [{"name": record.name.value, "phones": [phone.value for phone in record.phones]} for record in address_book.values()]
    return jsonify(contacts_list)

@app.route('/delete/<string:name>', methods=['DELETE'])
def delete_contact(name):
    if name in address_book:
        del address_book[name]
        save_to_file("contacts.json")
        return jsonify({"message": f"Contact {name} deleted successfully!"})
    return jsonify({"error": "Contact not found!"})

@app.route('/edit/<string:name>', methods=['POST'])
def edit_contact(name):
    new_name = request.form.get('new_name')
    new_phone = request.form.get('new_phone')
    record = address_book.search_record(name)
    if record:
        if new_name:
            record.name = Name(new_name)
        if new_phone:
            record.phones[0] = Phone(new_phone)  
        save_to_file("contacts.json")
        return jsonify({"message": f"Contact {name} updated successfully!"})
    return jsonify({"error": "Contact not found!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

