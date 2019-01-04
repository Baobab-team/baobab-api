from flask import url_for, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect

from app import app, db
from app.models.business import BusinessHour, Business, Address


class BaseModelView(ModelView):
    def is_accessible(self):
        # if not current_user.is_active or not current_user.is_authenticated:
        #     return False
        #
        # if current_user.super or current_user.staff:
        #     return True

        # return False

        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('/admin/login', next=request.url))

    can_export = True
    form_widget_args = {
        'created': {
            'disabled': True
        },
        'updated': {
            'disabled': True
        }
    }



class UserView(BaseModelView):
    pass

class OwnerUserView(BaseModelView):
    pass


class EndUserView(BaseModelView):
    pass


class DataClerkUserView(BaseModelView):
    pass


class BusinessView(BaseModelView):
    form_excluded_columns = ['ratings', ]


class BusinessHourView(BaseModelView):
    pass


class CategoryView(BaseModelView):
    pass


admin = Admin(app, name='baobab admin', template_mode='bootstrap3')
# admin.add_view(UserView(User, db.session))
admin.add_view(BusinessView(Business, db.session, category="Business"))
admin.add_view(ModelView(Address, db.session, category="Business"))
admin.add_view(ModelView(BusinessHour, db.session, category="Business"))
# admin.add_view(UserView(User, db.session))
