from flask import Blueprint, render_template, request

from core.dashboard.views import UserDashboard

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/user')


@dashboard_blueprint.route('/dashboard/<user_id>', methods=['POST', 'GET'])
def show(user_id):
    dashboard_handler = UserDashboard()
    user = dashboard_handler.handle_request(request, form=None, user_id=user_id)
    return render_template('dashboard/index.html', user=user)
