from django.urls import path
from .views import MobileNumberLoginView, CreateUserView, LogoutView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('login/', MobileNumberLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
