from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('fetch-users', views.fetchUsers, name='fetchUsers'),
    path('fetch-stocks', views.fetchStocks, name='fetchStocks'),
    path('fetch-orders', views.fetchOrders, name='fetchOrders'),
    path('transactions', views.Transactions, name='transactions'),
    path('fetch-user/<str:id>', views.FetchUser, name='fetchUser'),
    path('deposit', views.deposit, name='deposit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('buyStock', views.buyStock, name='buyStock'),
    path('sellStock', views.sellStock, name='sellStock'),
    
]