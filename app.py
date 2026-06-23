import os

from flask import Flask
from config import Config
from flask_login import LoginManager
from models import db
from models.user import User

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.quotes import quotes_bp
from routes.products import products_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(quotes_bp)
app.register_blueprint(products_bp)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', '0') == '1'
    )
