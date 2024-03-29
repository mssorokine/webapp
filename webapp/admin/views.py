from flask_login import current_user
from flask import Blueprint, render_template

from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required
def admin_index():
    title = "Admins panel"
    return render_template('admin/index.html', page_title=title)