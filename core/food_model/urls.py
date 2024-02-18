from django.urls import path
from . import views
from .views import Food_item_list, food_item, ShopOwnerView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'food_model'

urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.login_site, name='login'),
  path('signup/', views.register, name='register'),
  path('email_view/', views.email_view, name='email_view'),
  
  #admin
  path('admin_views/', views.admin_view, name='admin_views'),

  #shopOwner
  path('Register_form/', views.shopowner_register, name='owner_form'),
  path('restaurant_view/', views.restaurant_view, name='restaurant_view'),
  path('addfooditem/', views.addfood_item, name='addfooditem'),
  path('restaurants/<int:restaurant_id>/', Food_item_list.as_view(), name='fooditem_list'),
  path('delete/<int:pk>/', views.delete_food_item, name='delete_food_item'),
  path('edit/<int:pk>/', views.edit_food_item, name='edit_food_item'),
  path('shop_owner/', ShopOwnerView.as_view(), name='shop_owner_orders'),
  path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
  path('reject_order/<int:order_id>/', views.reject_order, name='reject_order'),

  #user
  path('restaurant/', views.restaurant, name='restaurant'),
  path('food_item/<int:restaurant_id>/', food_item.as_view(), name='food_item'),
  path('user_order_detail/', views.user_order_detail, name='user_order_detail'),
  
  #user_profile
  path('user_profile/', views.profile_enter, name='profile_enter'),
  path('profile_view/', views.profile_view, name='profile_view'),
  path('edit_profile_view/<int:pk>', views.edit_profile_view, name='edit_profile_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)