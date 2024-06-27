from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("activation/<uuid>/", views.ActivationView.as_view(), name="activation"),
    path("edit/profile/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("delete/profile/", views.ProfileDeleteView.as_view(), name="profile_delete"),
    path("delete/check/<uuid>/", views.ProfileDeleteCheckView.as_view(), name="delete_check"),
    path("change/password", views.ChangePasswordView.as_view(), name="password_change"),
    path("reset/password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("reset/password/check/<uuid>/", views.ResetPasswordCheckView.as_view(), name="reset_password_check"),
    path("reset/password/complete/<uuid>/", views.ResetPasswordCompleteView.as_view(), name="reset_password_complete"),
]


