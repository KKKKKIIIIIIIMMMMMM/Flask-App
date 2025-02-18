from flask import Blueprint

bp = Blueprint('main', __name__)

from kim_gallery.main import routes 