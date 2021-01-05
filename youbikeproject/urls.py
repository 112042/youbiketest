"""youbikeproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url,include
from project import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),                #首頁        （home_page）
    path('Sbike/', views.Sbike),          #站點搜尋      (Station_search)
    path('Dbike/', views.Dbike),          #區域搜尋      (Districts_search)
    path('RSbike/', views.RSbike),  #餐廳搜尋      (Restaurant_search)
    path('PDbike/',views.PDbike),         #產品搜尋      (Production_search)
    path('search_title/', views.search_title),         #站名搜尋      (search_title)
    path('station_title/', views.station_title),         #產品搜尋      (Production_search)

]+ static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
