from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import profile, main_profile, change_password, custom_login, register, delete_user, \
    AdvLogoutView, activate, pick_username
from django.contrib.auth import views as auth_views
app_name = "accounts"
urlpatterns = [
    # path("pick_username/", views.pick_username, name="pick-username"),

    path("pick_username/", pick_username, name="pick-username"),
    path('profile/', profile, name='profile'),
    path('main-profile/', main_profile, name='main_profile'),

    path('password-change/', change_password, name='password_change'),
    path('login/', custom_login, name='login'),
    path('register/', register, name='register'),
    path('delete_user/', delete_user, name='deleteuser'),

    path('logout/', AdvLogoutView, name='logout'),

    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='invalid_verify.html'),
        name='invalid_verify'
    ),

    path(
        'confirm_email/',
        TemplateView.as_view(template_name='registration/confirm_email.html'),
        name='confirm_email'
    ),

    # path('search/', item_search, name='search'),

    path('activate/<uidb64>/<token>', activate, name='activate'),

    path('password-change/', change_password, name='password_change'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
