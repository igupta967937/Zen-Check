from django.urls import path
from .  import views
from django.contrib.auth.views import LoginView, LogoutView

# define the urls (for each of the views)
app_name = 'zencheck'
urlpatterns = [
  path('', views.home, name='home'),
  path('home', views.home, name='home'),
  path('login', views.LoginViewCustom.as_view(template_name='zencheck/login.html'), name='login'),
  path('logout', views.LogoutViewCustom.as_view(template_name='zencheck/logout.html'), name='logout'),
  path('signup', views.signup, name='signup'),
  path('news', views.news, name='news'),  
  path('resources', views.resources, name='resources'),
  path('aboutus', views.aboutus, name='aboutus'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('wellbeing', views.wellbeing, name='wellbeing'),
  path('pulsecheck', views.pulsecheck, name='pulsecheck'),
  path('error', views.error, name='error'),
]