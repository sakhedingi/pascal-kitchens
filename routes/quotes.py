from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.quote import Quote, LineItem
from models.customer import Customer
from models.product import Product
from datetime import datetime
import uuid

quotes_bp = Blueprint('quotes', __name__)

def generate_quote_number():
    """Generate unique quote number"""
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = str(uuid.uuid4())[:8].upper()
    return f"PK-{date_str}-{random_str}"

@quotes_bp.route("/quotes")
@login_required
def list_quotes():
    page = request.args.get('page', 1, type=int)
    quotes = Quote.query.filter_by(designer_id=current_user.id).paginate(page=page, per_page=10)
    return render_template('quotes/list.html', quotes=quotes)

@quotes_bp.route("/quotes/create", methods=['GET', 'POST'])
@login_required
def create_quote():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        project_name = request.form.get('project_name')
        base_tier = request.form.get('base_tier', 'signature')
        
        # Create or get customer
        customer = Customer.query.filter_by(email=customer_email).first()
        if not customer:
            customer = Customer(
                name=customer_name,
                email=customer_email,
                phone=customer_phone
            )
            db.session.add(customer)
            db.session.commit()
        
        # Create quote
        quote = Quote(
            quote_number=generate_quote_number(),
            customer_id=customer.id,
            designer_id=current_user.id,
            base_tier=base_tier
        )
        
        db.session.add(quote)
        db.session.commit()
        
        flash(f'Quote {quote.quote_number} created!', 'success')
        return redirect(url_for('quotes.edit_quote', quote_id=quote.id))
    
    return render_template('quotes/create.html')

@quotes_bp.route("/quotes/<int:quote_id>/edit")
@login_required
def edit_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    
    # Check authorization
    if quote.designer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Get products grouped by category
    products_by_category = {}
    categories = ['BOARDS', 'HARDWARE', 'GLASS DOORS', 'STONE', 'SANITARY', 'LIGHTING']
    for category in categories:
        products_by_category[category] = Product.query.filter_by(category=category).all()
    
    return render_template('quotes/edit.html', quote=quote, products_by_category=products_by_category)

@quotes_bp.route("/quotes/<int:quote_id>/preview")
@login_required
def preview_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    
    # Check authorization
    if quote.designer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('quotes/preview.html', quote=quote)

@quotes_bp.route("/api/quotes/<int:quote_id>/line-items", methods=['POST'])
@login_required
def add_line_item(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    
    if quote.designer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    line_item = LineItem(
        quote_id=quote_id,
        description=data.get('description'),
        category=data.get('category'),
        unit=data.get('unit'),
        quantity=float(data.get('quantity', 1)),
        rate=float(data.get('rate', 0)),
        cost=float(data.get('cost', 0)) if data.get('cost') else None,
        tier_override=data.get('tier_override')
    )
    
    line_item.total = line_item.quantity * line_item.rate
    
    db.session.add(line_item)
    db.session.commit()
    
    return jsonify({'id': line_item.id, 'total': line_item.total}), 201

@quotes_bp.route("/api/quotes/<int:quote_id>/update-totals", methods=['POST'])
@login_required
def update_totals(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    
    if quote.designer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    quote.subtotal = float(data.get('subtotal', 0))
    quote.accessories = float(data.get('accessories', 0))
    quote.installation = float(data.get('installation', 0))
    quote.delivery = float(data.get('delivery', 3500))
    quote.vat = float(data.get('vat', 0))
    quote.total = float(data.get('total', 0))
    
    db.session.commit()
    
    return jsonify({'success': True})

@quotes_bp.route("/quotes/<int:quote_id>/delete", methods=['POST'])
@login_required
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    
    if quote.designer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    db.session.delete(quote)
    db.session.commit()
    
    flash('Quote deleted', 'info')
    return redirect(url_for('quotes.list_quotes'))
