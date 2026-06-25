from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("basic-test/", views.basic_test, name="basic_test"),
    path("advanced-test/", views.advanced_test, name="advanced_test"),
    path("results/", views.results, name="results"),
    path("register/", views.register_view, name="register"),
    path("verify-email/<int:user_id>/", views.verify_email_view, name="verify_email"),
    path("verify-email/<int:user_id>/resend/", views.resend_otp_view, name="resend_otp"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("feedback/", views.feedback_view, name="feedback"),
    
]
