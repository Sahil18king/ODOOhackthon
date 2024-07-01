from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup,name='signup'),
    path('loginform',views.loginform,name='loginform'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('create-password/<uidb64>/<token>/', views.create_password, name='create_password'),
    #  path('get-doctors-by-department/', views.get_doctors_by_department, name='get_doctors_by_department'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('business_signup/', views.business_signup, name='business_signup'),
    path('sell/', views.sell, name='sell'),
    path('deals/', views.deals, name='deals'),
    path('update_status/<int:listing_id>/', views.update_listing_status, name='update_listing_status'),
    
   
]
