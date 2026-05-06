from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('intervenciones/', include('intervenciones.urls')),
    path('jornada/', include('jornada.urls')),
]