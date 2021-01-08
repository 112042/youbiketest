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

#首頁的顯示
def index(request):
    #將index的所有功能放入index.html
    return render(request,'index.html')

#Sbike的顯示功能(站名初始畫面)
def Sbike(request):

    #將處理過的資料與要顯示的資料放入youbikes_information_station內
    #此資料存入下拉式選單的站名
    youbikes_information_station = []

    #抓取youbike的api
    youbike_url_station='http://210.61.47.192:80/youbike/api/youbike/station/availability'

    #youbike的api格式
    youbike_params_station = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    #將定義的格式與api的url放入r這個參數
    r = requests.get(youbike_url_station, params=youbike_params_station)
    
    #要求r用json的格式表達，並給予result
    results = r.json()

    #從result的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deal
    youbike_data_deal=results['data']
    
    #列youbike_data_deal中所有資料，並放入到result中
    for result in youbike_data_deal:

        #youbike_data_deal的資料型態為dictionary，固建立一個字典為youbike_data_station，並將result中的資料放入此字典
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
        
        #將建立的youbike_data_station存入要顯示的youbikes_information_station資料中
        youbikes_information_station.append(youbike_data_station)
   
   #將要顯示的資料統一放入context的參數中        
    context = {
        'youbikes' : youbikes_information_station
    }
    
    #將Sbike的所有功能放入station_search.html
    return render(request, 'station_search.html', context)

#station_title的搜尋功能(站名搜尋功能)
def station_title(request):
    
    #抓取前端name=sel_value的值（下拉式選單）
    search_name=request.GET.get("sel_value","")
    
    #將處理過的資料與要顯示的資料放入youbikes_information_station與youbikes_information_stationts內
    #此資料存入下拉式選單的站名
    youbikes_information_station = []

    #此資料存入要顯示的表格（根據search_name找尋的顯示值）
    youbikes_information_stationts=[]

   #抓取youbike的api
    youbike_url_station='http://210.61.47.192:80/youbike/api/youbike/station/availability'

    #youbike的api格式
    youbike_params_station = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    #將定義的格式與api的url放入r這個參數
    r = requests.get(youbike_url_station, params=youbike_params_station)

    #要求r用json的格式表達，並給予result
    results = r.json()

    #從result的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deal
    youbike_data_deal=results['data']

    #列youbike_data_deal中所有資料，並放入到result中
    for result in youbike_data_deal:

        #youbike_data_deal的資料型態為dictionary，固建立一個字典為youbike_data_station，並將result中的資料放入此字典
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

        #將建立的youbike_data_station存入要顯示的youbikes_information_station資料中
        youbikes_information_station.append(youbike_data_station)

        #將api上的經營字元轉換成"yes","no"（1="yes", 2="no"）
        if youbike_data_station['operation']=="1":
            youbike_data_station['operation']="yes"
        else:
            youbike_data_station['operation']="no"

        #將抓取的前端值（下拉式選單）並與youbike_data_station['name']比對
        if search_name == youbike_data_station['name']:

            #如果站名存在，就將資料傳入到youbikes_information_stationts
            youbikes_information_stationts.append(youbike_data_station)
    
    #將要顯示的資料統一放入context的參數中  
    context = {
        'youbikes':youbikes_information_station,
        'youbike_availability':youbikes_information_stationts
    }
    
    #將station_title的所有功能放入station_search.html
    return render(request, 'station_search.html', context)

#Dbike的顯示功能(區域初始畫面)  
def Dbike(request):

    #將處理過的資料與要顯示的資料放入youbikes_information_districts內
    #此資料存入下拉式選單的區域
    youbikes_information_districts = []

    #抓取youbike的api
    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    
    #youbike的api格式
    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    #將定義的格式與api的url放入r這個參數
    r = requests.get(youbike_url_districts, params=youbike_params_districts)

    #要求r用json的格式表達，並給予result
    results = r.json()

    #從result的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deal
    youbike_data_deal=results['data']
    
    #列youbike_data_deal中所有資料，並放入到result中
    for result in youbike_data_deal:
        
        #將要顯示的資料放入youbikes_information_districts中（api端將資料形勢已處理好，不用在處理）
        youbikes_information_districts.append(result)

    #將要顯示的資料統一放入context的參數中 
    context = {
        'youbikes' : youbikes_information_districts,
    }
    
    #將Dbike的所有功能放入station_search.html
    return render(request, 'districts_search.html', context)

#search_title的搜尋功能(區域的搜尋功能)
def search_title(request):

    #抓取前端name=sel_value的值（下拉式選單）
    search_name=request.GET.get("sel_value","")
    
    #將處理過的資料與要顯示的資料放入youbikes_information_station與youbikes_information_stationts內
    #此資料存入下拉式選單的區域
    youbikes_information_districts = []

    #此資料存入搜尋結果的區域
    youbikes_information_station = []

    #抓取youbike的api
    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    youbike_url_station='http://210.61.47.192:80/youbike/api/youbike/station/availability'

    #youbike的api格式
    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    #將定義的格式與api的url放入x這個參數
    x = requests.get(youbike_url_districts, params=youbike_params_districts)

    #要求x用json的格式表達，並給予resultss
    resultss = x.json()

    #從resultss的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deals
    youbike_data_deals=resultss['data']
    
    
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
    restaurant_information = []
    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    restaurant_url_districts='https://cuisine-final-project.herokuapp.com:443/api/restaurant/all'
    #restaurant_url_districts='https://data.ntpc.gov.tw/api/datasets/60D18399-A0F3-4C31-BF21-CEABFDC04CE7/json?page=0&size=10000'
    restaurant_params_districts =[] 

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
        z=result.strip(" Dist.")
        youbikes_information_districts.append(z)   

    r = requests.get(restaurant_url_districts, params=restaurant_params_districts)
    results = r.json()

    for x in youbikes_information_districts:
        for restaurant_data_deal in results:
            restaurant_data_select = {
                'id': restaurant_data_deal['id'], 
                'ownerId':restaurant_data_deal['ownerId'], 
                'name':restaurant_data_deal['name'], 
                'location':restaurant_data_deal['location'], 
                'startTime':restaurant_data_deal['startTime'], 
                'endTime':restaurant_data_deal['endTime'], 
                'website':restaurant_data_deal['website'], 
                'phone':restaurant_data_deal['phone'], 
                'image':restaurant_data_deal['image'],
                'introduction':restaurant_data_deal['introduction'], 
                'promotion':restaurant_data_deal['promotion'], 
                'created_at':restaurant_data_deal['created_at'], 
                'modified_at':restaurant_data_deal['modified_at']
                }

            pos=restaurant_data_select['location'].find(x)
            
            if pos>0:
                slector={
                    'd':x,
                    'add':restaurant_data_select['location'],
                    'n':restaurant_data_select['name']
                    }
                restaurant_information.append(slector)     
    
    context = {
        'youbikes':youbikes_information_districts,
        'restaurants' : restaurant_information
    }
    
    return render(request, 'restaurant_search.html', context)
    #return render(request, 'twst.html', context)


def restaurant_title(request):
    
    search_dis=request.GET.get("sel1","")     #抓取第一個值
    search_name=request.GET.get("sel2","")    #抓取第二個值

    #存擋資訊
    restaurant_information = []
    restaurant_table=[]
    Youbike_table=[]
    youbikes_information_districts = []
    youbikes_information = []

    #api來源
    youbike_url_availability='http://210.61.47.192:80/youbike/api/youbike/station/availability'
    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    restaurant_url_districts='https://cuisine-final-project.herokuapp.com:443/api/restaurant/all'
    
    #api的字典
    restaurant_params_districts =[] 
    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    #抓取第一個詳細的api
    x = requests.get(youbike_url_availability, params=youbike_params_districts)
    resultss = x.json()
    youbike_data_deals=resultss['data']
    
    for result in youbike_data_deals:
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
        z=youbike_data_station['area'].strip(" Dist.")
        youbikes_information_districts.append(z) 
    
    #抓取第二個api(區域)
    y = requests.get(youbike_url_districts, params=youbike_params_districts)
    resultsss = y.json()
    youbike_data_dealss=resultsss['data']
    
    for result in youbike_data_dealss:
        z=result.strip(" Dist.")
        youbikes_information.append(z)  


    #抓取第三個api並整合到前端(下拉式的部分)
    r = requests.get(restaurant_url_districts, params=restaurant_params_districts)
    results = r.json()
    
    for x in youbikes_information:
        for restaurant_data_deal in results:
            restaurant_data_select = {
                'id': restaurant_data_deal['id'], 
                'ownerId':restaurant_data_deal['ownerId'], 
                'name':restaurant_data_deal['name'], 
                'location':restaurant_data_deal['location'], 
                'startTime':restaurant_data_deal['startTime'], 
                'endTime':restaurant_data_deal['endTime'], 
                'website':restaurant_data_deal['website'], 
                'phone':restaurant_data_deal['phone'], 
                'image':restaurant_data_deal['image'],
                'introduction':restaurant_data_deal['introduction'], 
                'promotion':restaurant_data_deal['promotion'], 
                'created_at':restaurant_data_deal['created_at'], 
                'modified_at':restaurant_data_deal['modified_at']
                }
           
            pos=restaurant_data_select['location'].find(x)
            
            if pos>0:
                slector={
                    'd':x,
                    'add':restaurant_data_select['location'],
                    'n':restaurant_data_select['name']
                    }
                restaurant_information.append(slector)

    #餐廳的顯示處理
    for restaurant_data_deal in results:
            restaurant_data_select = {
                'id': restaurant_data_deal['id'], 
                'ownerId':restaurant_data_deal['ownerId'], 
                'name':restaurant_data_deal['name'], 
                'location':restaurant_data_deal['location'], 
                'startTime':restaurant_data_deal['startTime'], 
                'endTime':restaurant_data_deal['endTime'], 
                'website':restaurant_data_deal['website'], 
                'phone':restaurant_data_deal['phone'], 
                'image':restaurant_data_deal['image'],
                'introduction':restaurant_data_deal['introduction'], 
                'promotion':restaurant_data_deal['promotion'], 
                'created_at':restaurant_data_deal['created_at'], 
                'modified_at':restaurant_data_deal['modified_at']
                }

            if len(search_name)==0:
                
                pos4=restaurant_data_select['location'].find(search_dis)
                
                if pos4>=0:
                    rtable={
                        'n':restaurant_data_select['name'],
                        'lo':restaurant_data_select['location'],
                        'ph':restaurant_data_select['phone'],
                        'pro':restaurant_data_select['promotion'],
                        'intro':restaurant_data_select['introduction']
                    }
                    restaurant_table.append(rtable)

            else:
                pos2=restaurant_data_select['name'].find(search_name)
                
                if pos2>=0 :
                    rtable={
                        'n':restaurant_data_select['name'],
                        'lo':restaurant_data_select['location'],
                        'ph':restaurant_data_select['phone'],
                        'pro':restaurant_data_select['promotion'],
                        'intro':restaurant_data_select['introduction']
                    }
                    restaurant_table.append(rtable)
           
                
    
    for result in youbike_data_deals:
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

        if len(search_name)!=0:
            pos3=youbike_data_station['area'].find(search_dis)
            if pos3>=0:
                Youbike_table.append(youbike_data_station)

   
    context = {
        'youbikes':youbikes_information,
        'ybike':youbikes_information_districts,
        'restaurants' : restaurant_information,
        'rt':restaurant_table,
        'yt':Youbike_table
        
    }
    
    return render(request, 'restaurant_search.html', context)
    #return render(request,'twst.html',context)


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
