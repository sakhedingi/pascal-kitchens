from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.quote import Quote

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/")
@login_required
def dashboard():
    # Get stats for the current user
    total_quotes = Quote.query.filter_by(designer_id=current_user.id).count()
    pending_quotes = Quote.query.filter_by(designer_id=current_user.id, status='draft').count()
    accepted_quotes = Quote.query.filter_by(designer_id=current_user.id, status='accepted').count()
    rejected_quotes = Quote.query.filter_by(designer_id=current_user.id, status='rejected').count()
    
    return render_template(
        'dashboard.html',
        total_quotes=total_quotes,
        pending_quotes=pending_quotes,
        accepted_quotes=accepted_quotes,
        rejected_quotes=rejected_quotes
    )
