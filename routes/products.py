from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.product import Product

products_bp = Blueprint('products', __name__)

@products_bp.route("/products")
@login_required
def products():
    category = request.args.get('category', 'BOARDS')
    tier = request.args.get('tier', 'signature')
    
    query = Product.query.filter_by(category=category)
    if tier:
        query = query.filter_by(tier=tier)
    
    products = query.all()
    categories = ['BOARDS', 'HARDWARE', 'GLASS DOORS', 'STONE', 'SANITARY', 'LIGHTING']
    tiers = ['essential', 'signature', 'luxury', 'premium']
    
    return render_template(
        'products/list.html',
        products=products,
        categories=categories,
        tiers=tiers,
        current_category=category,
        current_tier=tier
    )

@products_bp.route("/api/products", methods=['GET'])
@login_required
def api_products():
    category = request.args.get('category')
    tier = request.args.get('tier')
    
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    if tier:
        query = query.filter_by(tier=tier)
    
    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'tier': p.tier,
        'unit': p.unit,
        'rate': p.rate,
        'cost': p.cost
    } for p in products])

@products_bp.route("/api/products", methods=['POST'])
@login_required
def create_product():
    # Admin-only - can extend with role check
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    
    data = request.get_json()
    
    product = Product(
        name=data.get('name'),
        category=data.get('category'),
        tier=data.get('tier'),
        unit=data.get('unit', 'ea'),
        rate=float(data.get('rate')),
        cost=float(data.get('cost')) if data.get('cost') else None
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'id': product.id}), 201
