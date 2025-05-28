from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'BiblioApp'  

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='BiblioApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='BiblioApp:login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-collection/', views.add_collection, name='add_collection'),
    path('collection/<int:collection_id>/', views.view_collection, name='view_collection'),
    path('references/add/', views.create_reference, name='create_reference'),
]
