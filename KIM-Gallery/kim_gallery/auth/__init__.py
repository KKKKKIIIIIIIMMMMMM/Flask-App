from flask import Blueprint

bp = Blueprint('auth', __name__)

from kim_gallery.auth import routes 