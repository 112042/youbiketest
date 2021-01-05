import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse   #基本的伺服器回復
from django.http import HttpResponseRedirect   #伺服器的路徑進行重定向
from django.contrib import auth              #導入Django內建認證函數
from django.contrib.auth.decorators import login_required              #導入Django login_requirement
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User, Group
from json import dumps

# Create your views here.

#首頁
def index(request):
    return render(request,'index.html')

def Sbike(request):
    youbikes_information_station = []

    youbike_url_station='http://210.61.47.192:80/youbike/api/youbike/station/availability'

    youbike_params_station = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    r = requests.get(youbike_url_station, params=youbike_params_station)
    results = r.json()
    youbike_data_deal=results['data']
    #youbikes_information.append(youbike_data_deal)
    

    for result in youbike_data_deal:
        youbike_data_station = {
            'id':result['sno'],
            'name':result['sna'],
            'area':result['sarea'],
            'address':result['ar'],
            'operation':result['act'],
            'parking':result['tot'],
            'brrow':result['sbi'],
            'free':result['bemp'],
            'update':result['mday']   
            }
        
        youbikes_information_station.append(youbike_data_station)
   

    
        
    context = {
        'youbikes' : youbikes_information_station
    }
    
    return render(request, 'station_search.html', context)
    #return render(request,'index.html')

def station_title(request):
    #search_name=request.GET.get("title","")
    search_name=request.GET.get("sel_value","")
    youbikes_information_station = []
    youbikes_information_stationts=[]

    #youbike_url_stations='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    youbike_url_station='http://210.61.47.192:80/youbike/api/youbike/station/availability'

    
    youbike_params_station = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    r = requests.get(youbike_url_station, params=youbike_params_station)
    results = r.json()
    youbike_data_deal=results['data']
    #youbikes_information.append(youbike_data_deal)
    

    for result in youbike_data_deal:
        youbike_data_station = {
            'id':result['sno'],
            'name':result['sna'],
            'area':result['sarea'],
            'address':result['ar'],
            'operation':result['act'],
            'parking':result['tot'],
            'brrow':result['sbi'],
            'free':result['bemp'],
            'update':result['mday']   
            }
        youbikes_information_stationts.append(youbike_data_station)

    for result in youbike_data_deal:
        youbike_data_station = {
            'id':result['sno'],
            'name':result['sna'],
            'area':result['sarea'],
            'address':result['ar'],
            'operation':result['act'],
            'parking':result['tot'],
            'brrow':result['sbi'],
            'free':result['bemp'],
            'update':result['mday']   
            }
        if youbike_data_station['operation']=="1":
            youbike_data_station['operation']="yes"
        else:
            youbike_data_station['operation']="no"

        if search_name == youbike_data_station['name']:
            youbikes_information_station.append(youbike_data_station)
        #book_list=youbikes_information_station.objects.filter(title__contains=search_name) 
    
    context = {
        'youbikes' : youbikes_information_stationts,
        'youbike_availability':youbikes_information_station
    }
    
    return render(request, 'station_search.html', context)
    
def Dbike(request):
    
    # youbikes_information = []
    
    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    #youbike_url_availability='http://210.61.47.192:80/youbike/api/youbike/station/availability'
    
    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    r = requests.get(youbike_url_districts, params=youbike_params_districts)
    results = r.json()
    youbike_data_deal=results['data']
    
    youbikes_information_districts = []

    for result in youbike_data_deal:
            youbikes_information_districts.append(result)
         
            
    #if request.method == 'POST':    #針對index網頁上提交的表單行為，做處理
    #area=request.POST.get('search_button','')    #針對index網頁提交的username的資料，取得username的資訊
        #username=request.session.get('user','')
    #search_area=request.GET.get("search_button","")
        
    #youbike_params_availability = {
     #   'status': 'status',
     #   'message': 'message',
     #   'data': 'data'
     #   }

    #x = requests.get(youbike_url_availability, params=youbike_params_availability)
    #resultss = x.json()
    #youbike_data_deals=resultss['data']

    #for result in youbike_data_deals:
        #for i, result in enumerate(youbike_data_deal):
       # youbike_data_available = {
          #  'title':result['sno'],
          #  'name':result['sna'],
          #  'area':result['sarea'],
          #  'address':result['ar'],
          #  'operation':result['act'],
          #  'update':result['mday']   
          #  }
       # youbikes_information.append(youbike_data_available)
        
    
    context = {
        'youbikes' : youbikes_information_districts,
        #'youbike_availability':youbikes_information,
    }
    
    return render(request, 'districts_search.html', context)
    #return render(request, 'twst.html', context)
    #return render(request,'index.html')

def search_title(request):
    #search_name=request.GET.get("title","")
    search_name=request.GET.get("sel_value","")
    youbikes_information_station = []

    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    youbike_url_station='http://210.61.47.192:80/youbike/api/youbike/station/availability'


    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    x = requests.get(youbike_url_districts, params=youbike_params_districts)
    resultss = x.json()
    youbike_data_deals=resultss['data']
    
    youbikes_information_districts = []

    for result in youbike_data_deals:
            youbikes_information_districts.append(result)   
    
    youbike_params_station = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    r = requests.get(youbike_url_station, params=youbike_params_station)
    results = r.json()
    youbike_data_deal=results['data']
    #youbikes_information.append(youbike_data_deal)
    

    for result in youbike_data_deal:
        youbike_data_station = {
            'id':result['sno'],
            'name':result['sna'],
            'area':result['sarea'],
            'address':result['ar'],
            'operation':result['act'],
            'parking':result['tot'],
            'brrow':result['sbi'],
            'free':result['bemp'],
            'update':result['mday']   
            }
        if youbike_data_station['operation']=="1":
            youbike_data_station['operation']="yes"
        else:
            youbike_data_station['operation']="no"

        if search_name == youbike_data_station['area']:
            youbikes_information_station.append(youbike_data_station)
        #book_list=youbikes_information_station.objects.filter(title__contains=search_name) 
    
    context = {
        'youbikes' : youbikes_information_districts,
        'youbike_availability':youbikes_information_station,
    }
    
    return render(request, 'districts_search.html', context)



def RSbike(request):

    restaurant_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    #youbike_url_availability='http://210.61.47.192:80/youbike/api/youbike/station/availability'
    
    restaurant_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    r = requests.get(restaurant_url_districts, params=restaurant_params_districts)
    results = r.json()
    restaurant_data_deal=results['data']
    
    restaurant_information_districts = []

    for result in restaurant_data_deal:
            restaurant_information_districts.append(result)
         
    
    context = {
        'restaurants' : restaurant_information_districts,
        #'youbike_availability':youbikes_information,
    }
    
    return render(request, 'restaurant_search.html', context)
    #return render(request,'index.html')

def PDbike(request):
    youbikes_information_districts = []

    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'

    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    r = requests.get(youbike_url_districts, params=youbike_params_districts)
    results = r.json()
    youbike_data_deal=results['data']
    #youbikes_information.append(youbike_data_deal)
    

    #for result in youbike_data_deal:
    for i, result in enumerate(youbike_data_deal):
        youbike_data_districts = {
            #'title':result['sno'],
            #'name':result['sna'],
            'i':i,
            'area':result,
            #'address':result['ar'],
            #'operation':result['act'],
            #'update':result['mday']   
            }
        
        youbikes_information_districts.append(youbike_data_districts)
   

    
        
    context = {
        'youbikes' : youbikes_information_districts
    }
    
    return render(request, 'production_search.html', context)
    #return render(request,'index.html')