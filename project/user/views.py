from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from datetime import datetime 
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from .models import UserLoginLogout, User
from django.contrib.auth import login
from allauth.account.forms import LoginForm
from allauth.account import app_settings
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import get_next_redirect_url, passthrough_next_redirect_url
from allauth.utils import get_request_param, get_form_class
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import FormView
from allauth.account.views import RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, sensitive_post_parameters_m

class LoginView(RedirectAuthenticatedUserMixin,
                AjaxCapableProcessFormViewMixin,
                FormView):
    form_class = LoginForm
    template_name = "account/login." + app_settings.TEMPLATE_EXTENSION
    success_url = None
    redirect_field_name = "next"

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'login', self.form_class)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(
            self.request,
            self.redirect_field_name) or self.success_url)
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("account_signup"),
                                                   self.redirect_field_name)
        redirect_field_value = get_request_param(self.request,
                                                 self.redirect_field_name)
        site = get_current_site(self.request)

        ret.update({"signup_url": signup_url,
                    "site": site,
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret

def user_login_time(request, **kwargs):
    x = datetime.now()
    try:
        user = UserLoginLogout.objects.get(USER = request.user, DATE = x.date())
    except: 
        user = UserLoginLogout.objects.create(USER = request.user, DATE = x.date(), LOGIN = x.time())
    return user

def user_logout_time(request, **kwargs):
    x = datetime.now()
    user = UserLoginLogout.objects.get(USER = request.user, DATE = x.date())
    user.LOGOUT = x.time()
    user.save()
    return user

user_logged_in.connect(user_login_time)
user_logged_out.connect(user_logout_time)