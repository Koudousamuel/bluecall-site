from django.urls import path
from . import views
from .views import envoyer_email

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('mot-de-passe-oublie/', views.demander_reinitialisation, name='password_reset_request'),
    path('verification-code/', views.verifier_code_reset, name='verify_reset_code'),
    path('nouveau-mot-de-passe/', views.nouveau_mot_de_passe, name='set_new_password'),
    path('createsuperuser/', views.create_superuser_view),

]