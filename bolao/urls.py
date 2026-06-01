from django.urls import path
from . import views

app_name = 'bolao'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('palpites/', views.palpites_view, name='palpites'),
    path('palpites/eliminatorias/', views.palpites_eliminatorias_view, name='palpites_eliminatorias'),
    path('redefinir-pin/', views.redefinir_pin_view, name='redefinir_pin'),
    path('publico/', views.palpites_publicos_view, name='publico'),
    path('api/salvar-palpites/', views.salvar_palpites, name='salvar_palpites'),
    path('api/salvar-palpites-eliminatorias/', views.salvar_palpites_eliminatorias, name='salvar_palpites_eliminatorias'),

    # Admin
    path('admin/', views.admin_login_view, name='admin_login'),
    path('admin/painel/', views.admin_painel_view, name='admin_painel'),
    path('admin/eliminatorias/', views.admin_eliminatorias_view, name='admin_eliminatorias'),
    path('admin/salvar-resultado/', views.admin_salvar_resultado, name='admin_salvar_resultado'),
    path('admin/salvar-config/', views.admin_salvar_config, name='admin_salvar_config'),
    path('admin/definir-equipes/', views.admin_definir_equipes, name='admin_definir_equipes'),
    path('admin/gerar-pin/', views.admin_gerar_pin, name='admin_gerar_pin'),
    path('admin/salvar-classificacao/', views.admin_salvar_classificacao, name='admin_salvar_classificacao'),
    path('admin/salvar-extras/', views.admin_salvar_extras, name='admin_salvar_extras'),
    path('admin/logout/', views.admin_logout_view, name='admin_logout'),
]
