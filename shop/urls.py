"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from .views import Index
from django.conf import settings
from django.conf.urls.static import static
from .views import Cart
from .views import CheckOut
from .views import login
from .views import OrderView
from myapp.middlewares.auth import auth_middleware

urlpatterns = [
    path('admin', admin.site.urls),
    path('',Index.as_view(),name='homepage'),
    path('signup',views.signup),
    path('login',login.as_view(),name='login'),
    path('logout',views.logout,name='logout'),
    path('cart',Cart.as_view(),name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
