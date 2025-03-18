from flask import request, jsonify, render_template
from . import app
from .models import Record, Name, Phone, address_book
from .storage import save_to_file

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
        return jsonify({"message": f"Contact {name} added!"})
    return jsonify({"error": "Name and phone required!"})

@app.route('/contacts')
def get_contacts():
    contacts = [
        {"name": rec.name.value, "phones": [p.value for p in rec.phones]}
        for rec in address_book.values()
    ]
    return jsonify(contacts)

@app.route('/delete/<string:name>', methods=['DELETE'])
def delete_contact(name):
    if name in address_book:
        del address_book[name]
        save_to_file("contacts.json")
        return jsonify({"message": f"Contact {name} deleted!"})
    return jsonify({"error": "Contact not found!"})

@app.route('/edit/<string:name>', methods=['POST'])
def edit_contact(name):
    new_name = request.form.get('new_name')
    new_phone = request.form.get('new_phone')
    record = address_book.get(name)
    if record:
        if new_name:
            record.name = Name(new_name)
        if new_phone:
            record.phones[0] = Phone(new_phone)
        save_to_file("contacts.json")
        return jsonify({"message": f"Contact {name} updated!"})
    return jsonify({"error": "Contact not found!"})
