from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('logout/', views.AccountLogoutView.as_view(), name='logout'),
    path(r'profile/', views.Profile.as_view(), name='view_profile'),
    path(r'profile/edit/', views.Update.as_view(), name='edit_profile'),
    path('password_change/', views.AccountPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.AccountPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.AccountPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.AccountPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.AccountPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.AccountPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('create/<uidb64>/<token>/', views.AccountCreateView.as_view(), name='create_account'),
    path('create/done/', views.AccountCreationCompleteView.as_view(), name='account_creation_complete'),
    path('privacy/', views.privacy_statement, name='privacy_statement'),
]
