from datetime import datetime
from extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(50), nullable=False, default='general')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
