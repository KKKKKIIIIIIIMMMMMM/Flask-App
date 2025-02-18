from app import create_app, db
from app.models.user import User
from app.models.image import Image, Tag
from app.models.comment import Comment

app = create_app()
with app.app_context():
    db.create_all()