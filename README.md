# Pascal Kitchens — Quote Studio

A professional Flask-based quote generation system for Pascal Kitchens, a premium kitchen design and installation company.

## Project Structure

```
pascal-kitchens/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── models/                # Database models
│   ├── __init__.py
│   ├── user.py
│   ├── customer.py
│   ├── product.py
│   └── quote.py
├── routes/                # API routes and views
│   ├── auth.py
│   ├── dashboard.py
│   ├── quotes.py
│   └── products.py
├── templates/             # Jinja2 templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── quotes/
│       ├── create.html
│       ├── list.html
│       ├── edit.html
│       └── preview.html
├── static/                # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── instance/              # Instance folder (database)
└── uploads/               # File uploads

```

## Features

### Authentication
- User registration and login
- Session management with Flask-Login
- Role-based access (designer, admin, client)

### Quote Management
- Create new quotes with customer information
- Select pricing tiers (Essential, Signature, Luxury, Premium)
- Add line items from product catalogue
- Real-time preview pane
- Save quotes to database
- View all quotes with filtering and pagination
- Delete quotes

### Product Catalogue
- Organized by category (BOARDS, HARDWARE, GLASS DOORS, STONE, SANITARY, LIGHTING)
- Tier-based pricing
- Unit pricing and cost tracking
- Filter by category and tier

### Quote Preview
- Professional quote format
- Client information
- Itemized breakdown
- Pricing calculations (subtotal, accessories, installation, delivery, VAT)
- Print-to-PDF capability
- Email sending (future milestone)

### Designer Features
- Dashboard with quote statistics
- Margin tracking (cost vs. sell price)
- Quote templates and customization
- Customer history

## Setup & Installation

1. **Clone the repository**
   ```bash
   cd pascal-kitchens
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python3 app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Default Credentials

For development:
- Username: `admin`
- Email: `admin@pascalkitchens.com`
- Password: `admin123`

(Create an account during registration for real usage)

## Database

The application uses SQLite for local development. The database file is stored in the `instance/` folder as `pascal.db` and is created automatically on first run.

## Configuration

Edit `config.py` to modify:
- Secret key for session management
- Database URI
- File upload limits
- CSRF protection

## Milestones

1. ✅ **Milestone 1** — Authentication (register, login, logout)
2. ✅ **Milestone 2** — Dashboard with statistics
3. ✅ **Milestone 3** — Quote Studio with product catalogue
4. ⏳ **Milestone 4** — Product catalogue with image uploads
5. ⏳ **Milestone 5** — PDF quote generation (advanced)
6. ⏳ **Milestone 6** — Email quotations
7. ⏳ **Milestone 7** — Installation calendar
8. ⏳ **Milestone 8** — Customer portal
9. ⏳ **Milestone 9** — Analytics and reporting
10. ⏳ **Milestone 10** — Automated tests with pytest

## Technologies

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Security**: Werkzeug password hashing, CSRF protection

## Deployment (Render)

1. Push your code to GitHub.
2. In Render, create a new **Web Service** from your repository.
3. Configure commands:
   - **Build Command**: `python3 -m pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add environment variables:
   - `SECRET_KEY` = a long random secret string
   - `FLASK_DEBUG` = `0`

The app is configured to bind to `0.0.0.0` and read `PORT` from the environment for cloud hosting.

## License

© 2026 Pascal Kitchens. All rights reserved.
