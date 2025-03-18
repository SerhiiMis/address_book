import json
from .models import Record, address_book

def load_from_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for name, record_data in data.items():
                record = Record(name)
                for phone in record_data["phones"]:
                    record.add_phone(phone)
                address_book.add_record(record)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_to_file(filename):
    with open(filename, "w") as file:
        data = {
            name: {"phones": [phone.value for phone in record.phones]}
            for name, record in address_book.items()
        }
        json.dump(data, file, indent=4)
