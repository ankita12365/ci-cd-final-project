from flask import Flask
from service.models import Product
from service.common import status

app = Flask(__name__)

from service import routes
from service.common import error_handlers
