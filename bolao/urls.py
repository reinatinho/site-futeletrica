from django.urls import path
from . import views

app_name = 'bolao'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('palpites/', views.palpites_view, name='palpites'),
    path('publico/', views.palpites_publicos_view, name='publico'),
    path('api/salvar-palpites/', views.salvar_palpites, name='salvar_palpites'),

    # Admin
    path('admin/', views.admin_login_view, name='admin_login'),
    path('admin/painel/', views.admin_painel_view, name='admin_painel'),
    path('admin/salvar-resultado/', views.admin_salvar_resultado, name='admin_salvar_resultado'),
    path('admin/salvar-config/', views.admin_salvar_config, name='admin_salvar_config'),
    path('admin/logout/', views.admin_logout_view, name='admin_logout'),
]
