from models import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # BOARDS, HARDWARE, GLASS, STONE, SANITARY, LIGHTING
    tier = db.Column(db.String(50), nullable=False)  # essential, signature, luxury, premium
    unit = db.Column(db.String(30), default='ea')  # ea, m², lin.m, unit, set, etc.
    rate = db.Column(db.Float, nullable=False)  # Sell price
    cost = db.Column(db.Float)  # Cost price
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Product {self.name}>'
