from flask import request, jsonify, render_template
from . import app, db
from .models import Contact

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    if name and phone:
        new_contact = Contact(name=name, phone=phone)
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": f"Contact {name} added!"})
    return jsonify({"error": "Name and phone required!"})

@app.route('/contacts')
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{"name": c.name, "phone": c.phone} for c in contacts])

@app.route('/delete/<string:name>', methods=['DELETE'])
def delete_contact(name):
    contact = Contact.query.filter_by(name=name).first()
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": f"Contact {name} deleted!"})
    return jsonify({"error": "Contact not found!"})

@app.route('/edit/<string:name>', methods=['POST'])
def edit_contact(name):
    contact = Contact.query.filter_by(name=name).first()
    if not contact:
        return jsonify({"error": "Contact not found!"})
    
    new_name = request.form.get('new_name')
    new_phone = request.form.get('new_phone')
    if new_name:
        contact.name = new_name
    if new_phone:
        contact.phone = new_phone
    db.session.commit()
    return jsonify({"message": f"Contact {name} updated!"})
