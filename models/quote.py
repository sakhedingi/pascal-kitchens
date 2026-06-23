from models import db

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    designer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    base_tier = db.Column(db.String(50), default='signature')  # essential, signature, luxury, premium
    
    subtotal = db.Column(db.Float, default=0.0)
    accessories = db.Column(db.Float, default=0.0)
    installation = db.Column(db.Float, default=0.0)
    delivery = db.Column(db.Float, default=3500.0)
    vat = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(50), default='draft')  # draft, sent, accepted, rejected, installed
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relationships
    designer = db.relationship('User', backref='quotes')
    line_items = db.relationship('LineItem', backref='quote', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Quote {self.quote_number}>'


class LineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50))
    unit = db.Column(db.String(30))
    quantity = db.Column(db.Float, default=1.0)
    rate = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    cost = db.Column(db.Float)  # Cost for margin tracking
    total = db.Column(db.Float, default=0.0)
    tier_override = db.Column(db.String(50))  # Override tier for this line
    
    def __repr__(self):
        return f'<LineItem {self.description}>'
