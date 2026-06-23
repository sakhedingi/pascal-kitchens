from models import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(30))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Relationship to quotes
    quotes = db.relationship('Quote', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'
