from django.urls import path
from . import views

app_name = 'bolao'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login_alt'),
    path('logout/', views.logout_view, name='logout'),
    path('palpites/', views.palpites_view, name='palpites'),
    path('api/salvar-palpites/', views.salvar_palpites, name='salvar_palpites'),
]
