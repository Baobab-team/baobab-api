from flask import url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user
from werkzeug.utils import redirect


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


class LoginMenuLink(MenuLink):

    def is_accessible(self):
        return not current_user.is_authenticated


class BaseModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.super or current_user.staff:
            return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('/admin/login', next=request.url))

    can_export = True


class UserView(BaseModelView):
    column_default_sort = ['name', 'phone', 'email', 'website', 'description', 'date_created', 'date_modified']
    column_exclude_list = ['_password', ]
    column_filters = ['active']
    column_searchable_list = ["email"]


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
    form_excluded_columns = ['date_created', 'date_modified', 'businesses']
