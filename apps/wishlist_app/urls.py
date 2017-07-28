from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='wishlist_app_index'),
    url(r'^register$', views.register, name='wishlist_app_register'),
    url(r'^login$', views.login, name='wishlist_app_login'),
    url(r'^home$', views.home, name='wishlist_app_home'),
    url(r'^addItem$', views.addItem, name='addItem'),
    url(r'^addToWishlist$', views.addToWishlist, name='addToWishlist'),
    url(r'^(?P<item_id>\d+)/addToMyItems$', views.addToMyItems, name='addToMyItems'),
    url(r'^(?P<item_id>\d+)/deleteItem$', views.deleteItem, name='deleteItem'),
    url(r'^(?P<item_id>\d+)/items$', views.items, name='items'),
    
    url(r'^reset$', views.reset, name='wishlist_app_reset'),
    
]