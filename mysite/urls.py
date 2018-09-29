from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from mysite.core import views as core_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^signup/$', core_views.signup, name='signup'),
	url(r'^login/$',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
	url(r'^logout/$',auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
	url(r'^search/$', core_views.search, name='search'),
	url(r'^restview/(?P<value>\S+)/', core_views.showRestaurantDetails, name='restview'),
	url(r'^submit/$', core_views.submit, name='submit')
	#url(r'^restview', 'core_views.showRestaurantDetails', name='restview') 
]

