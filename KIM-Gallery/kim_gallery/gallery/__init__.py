from flask import Blueprint

bp = Blueprint('gallery', __name__)

from kim_gallery.gallery import routes 