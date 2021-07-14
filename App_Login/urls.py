from django.urls import path
from App_Login import views

app_name = 'App_Login'

urlpatterns = [
        path('sign_up/', views.sign_up, name='sign_up'),
        path('login/', views.login_user, name='login'),
        path('logout/', views.logout_user, name='logout'),
        path('profile/', views.user_profile, name='profile'),
]