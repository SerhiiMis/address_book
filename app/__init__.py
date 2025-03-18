from flask import Flask
from .storage import load_from_file
from .models import address_book

app = Flask(__name__)

# Load contacts on startup
load_from_file("contacts.json")

from . import routes
