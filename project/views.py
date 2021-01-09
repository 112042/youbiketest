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
    
    #從resultss的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deals
    for result in youbike_data_deals:
            youbikes_information_districts.append(result)   
    
    #將定義的格式與api的url放入r這個參數
    r = requests.get(youbike_url_station, params=youbike_params_districts)

    #要求r用json的格式表達，並給予results
    results = r.json()

    #從results的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deal
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

        #將api上的經營字元轉換成"yes","no"（1="yes", 2="no"）
        if youbike_data_station['operation']=="1":
            #將抓取的前端值（下拉式選單）並與youbike_data_station['area']比對
            if search_name == youbike_data_station['area']:
                youbikes_information_station.append(youbike_data_station)

    #將要顯示的資料統一放入context的參數中 
    context = {
        'youbikes' : youbikes_information_districts,
        'youbike_availability':youbikes_information_station,
        'ytitle':search_name
    }
    
    #將search_title的所有功能放入districts_search.html
    return render(request, 'districts_search.html', context)

#RSbike的顯示功能(餐廳初始畫面) 
def RSbike(request):

    #將處理過的資料與要顯示的資料放入restaurant_information與restaurant_params_districts內
    #此資料存入下拉式選單的區域（第一格）
    youbikes_information_districts = []

    #此資料存入下拉式選單的區域（第二格）
    restaurant_information = []

    #抓取api
    #抓取youbike的api
    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'

    #抓取restaurant的api
    restaurant_url_districts='https://cuisine-final-project.herokuapp.com:443/api/restaurant/all'
   
   #api格式
   #youbike的api格式
    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    #restaurant的api格式
    restaurant_params_districts =[]

    #youbike的資料處理
    #將定義的格式與api的url放入x這個參數
    x = requests.get(youbike_url_districts, params=youbike_params_districts)

    #要求x用json的格式表達，並給予resultss
    resultss = x.json()

    #從results的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deals
    youbike_data_deals=resultss['data']
    
    #列youbike_data_deals中所有資料，並放入到result中
    for result in youbike_data_deals:

        #為了精準搜尋，做字串分割，只取前面的值
        z=result.strip(" Dist.")

        #將處理好的資料，放入youbikes_information_districts
        youbikes_information_districts.append(z)   

    #將定義的格式與api的url放入r這個參數
    r = requests.get(restaurant_url_districts, params=restaurant_params_districts)

    #要求r用json的格式表達，並給予results
    results = r.json()

    #雙重下拉式選單的處理
    #列youbikes_information_districts中所有資料，並放入到x中
    for x in youbikes_information_districts:

         #列results中所有資料，並放入到restaurant_data_deal 中
        for restaurant_data_deal in results:

            #results的資料型態為dictionary，固建立一個字典為restaurant_data_select，並將restaurant_data_deal中的資料放入此字典
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

            #建立一個pos的參數
            #pos為將餐廳的資訊（restaurant_data_select['location']）與區域的站名（x）做比對，並回傳是否存在這個值
            pos=restaurant_data_select['location'].find(x)
            
            #如果存在這個值pos就會回傳>=0的數值
            if pos>0:

                #定義一個字典為slector，給予第二個下拉選單的值
                slector={
                    'd':x,
                    'add':restaurant_data_select['location'],
                    'n':restaurant_data_select['name']
                    }

                #將存在的值，放入restaurant_information內
                restaurant_information.append(slector)     
    
    #將要顯示的資料統一放入context的參數中
    context = {
        'youbikes':youbikes_information_districts,
        'restaurants' : restaurant_information
    }
    
    #將RSbike的所有功能放入restaurant_search.html
    return render(request, 'restaurant_search.html', context)

#restaurant_title的搜尋功能(餐廳搜尋畫面) 
def restaurant_title(request):
    
    #抓取前端下拉式選單的值
    #抓取第一個下拉式選單的值
    search_dis=request.GET.get("sel1","") 

    #抓取第二個下拉式值
    search_name=request.GET.get("sel2","")    

    #將處理過的資料與要顯示的資料放入restaurant_information、restaurant_params_districts、youbikes_information_districts 、
    # youbikes_information、restaurant_table、Youbike_table
    
    #此資料存入下拉式選單的區域（第一格）
    youbikes_information = []

    #此資料存入下拉式選單的區域（第二格）
    restaurant_information = []
    
    #處理youbike顯示的資料，並存入youbikes_information_district
    # (在前端上，多一個資料參數，避免雙重迴圈導致資料顯示過多)
    youbikes_information_districts = []
    
    #處理表格顯示的資料
    #顯示餐廳處理的資料
    restaurant_table=[]

    #顯示youbike處理的資料
    Youbike_table=[]

    #api來源
    youbike_url_availability='http://210.61.47.192:80/youbike/api/youbike/station/availability'
    youbike_url_districts='http://210.61.47.192:80/youbike/api/youbike/station/districts'
    restaurant_url_districts='https://cuisine-final-project.herokuapp.com:443/api/restaurant/all'
    
    #api格式
    #youbike的api格式
    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    
    #restaurant的api格式
    restaurant_params_districts =[] 
    
    #youbike的資料處理-此部分特意針對多重顯示問題做處理
    #將定義的格式與api的url放入x這個參數
    x = requests.get(youbike_url_availability, params=youbike_params_districts)

    #要求x用json的格式表達，並給予resultss
    resultss = x.json()

    #從resultss的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deals
    youbike_data_deals=resultss['data']
    
    #列result中所有資料，並放入到youbike_data_deals 中
    for result in youbike_data_deals:

        #youbike_data_deals的資料型態為dictionary，固建立一個字典為youbike_data_station，並將result中的資料放入此字典
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

        #為了精準搜尋，做字串分割，只取前面的值
        z=youbike_data_station['area'].strip(" Dist.")

        #將處理好的資料，放入youbikes_information_districts
        youbikes_information_districts.append(z) 
    
    #youbike的資料處理-此部分特意針對第一個選單處理
    #將定義的格式與api的url放入y這個參數
    y = requests.get(youbike_url_districts, params=youbike_params_districts)

    #要求y用json的格式表達，並給予resultsss
    resultsss = y.json()

    #從resultsss的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_dealss
    youbike_data_dealss=resultsss['data']
    
    #列result中所有資料，並放入到youbike_data_dealss 中
    for result in youbike_data_dealss:

        #為了精準搜尋，做字串分割，只取前面的值
        z=result.strip(" Dist.")

        #將處理好的資料，放入youbikes_information
        youbikes_information.append(z)  


     #將定義的格式與api的url放入r這個參數)
    r = requests.get(restaurant_url_districts, params=restaurant_params_districts)

    #要求r用json的格式表達，並給予results
    results = r.json()
    
    #雙重下拉式選單的處理
    #列youbikes_information中所有資料，並放入到x中
    for x in youbikes_information:

        #列restaurant_data_deal中所有資料，並放入到results中
        for restaurant_data_deal in results:

            #results的資料型態為dictionary，固建立一個字典為restaurant_data_select，並將restaurant_data_deal中的資料放入此字典
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
           
            #建立一個pos的參數
            #pos為將餐廳的資訊（restaurant_data_select['location']）與區域的站名（x）做比對，並回傳是否存在這個值
            pos=restaurant_data_select['location'].find(x)
            
            #如果存在這個值pos就會回傳>=0的數值
            if pos>0:

                #定義一個字典為slector，給予第二個下拉選單的值
                slector={
                    'd':x,
                    'add':restaurant_data_select['location'],
                    'n':restaurant_data_select['name']
                    }

                #將存在的值，放入restaurant_information內
                restaurant_information.append(slector)

    #餐廳的Table顯示處理
    #列results中所有資料，並放入到restaurant_data_deal中
    for restaurant_data_deal in results:

            #results的資料型態為dictionary，固建立一個字典為restaurant_data_select，並將restaurant_data_deal中的資料放入此字典
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

            #判定前端有沒有輸入任何訊息（判定有沒有選擇餐廳）
            #沒有輸入餐廳
            if len(search_name)==0:
                
                #例外處理（只存入不顯示）
                #建立一個pos4的參數
                #pos4為將餐廳的資訊（restaurant_data_select['location']）與區域的站名（search_dis）做比對，並回傳是否存在這個值
                pos4=restaurant_data_select['location'].find(search_dis)
                
                #如果不存在，依然建立字典，此字典為空字典（不顯示）
                if pos4>=0:
                    rtable={
                        'n':restaurant_data_select['name'],
                        'lo':restaurant_data_select['location'],
                        'ph':restaurant_data_select['phone'],
                        'pro':restaurant_data_select['promotion'],
                        'intro':restaurant_data_select['introduction']
                    }
                    restaurant_table.append(rtable)

            #有輸入餐廳
            else:
                #建立一個pos2的參數
                #pos2為將餐廳的資訊（restaurant_data_select['name']）與區域的站名（search_names）做比對，並回傳是否存在這個值
                pos2=restaurant_data_select['name'].find(search_name)
                
                #如果存在，建立字典rtable
                if pos2>=0 :
                    rtable={
                        'n':restaurant_data_select['name'],
                        'lo':restaurant_data_select['location'],
                        'ph':restaurant_data_select['phone'],
                        'pro':restaurant_data_select['promotion'],
                        'intro':restaurant_data_select['introduction']
                    }
                    restaurant_table.append(rtable)
           
    #餐廳的Youbikie顯示處理
    #列youbike_data_deals中所有資料，並放入到result中
    for result in youbike_data_deals:

        #results的資料型態為dictionary，固建立一個字典為youbike_data_station，並將youbike_data_deals中的資料放入此字典
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

        #將api上的經營字元轉換成"yes","no"（1="yes", 2="no"）
        if youbike_data_station['operation']=="1":
             #判定前端有沒有輸入任何訊息（判定有沒有選擇餐廳）
            #有輸入餐廳
            if len(search_name)!=0:
                #建立一個pos3的參數
                #pos3為將餐廳的資訊（restaurant_data_select['area']）與區域的站名（search_dis）做比對，並回傳是否存在這個值
                pos3=youbike_data_station['area'].find(search_dis)
                
                #如果存在，存入要顯示的參數
                if pos3>=0:
                    Youbike_table.append(youbike_data_station)

       

    #將要顯示的資料統一放入context的參數中
    context = {
        'youbikes':youbikes_information,
        'restaurants' : restaurant_information,
        'rt':restaurant_table,
        'yt':Youbike_table,
        'dis':search_dis,
        'rname':search_name    
    }
    
    #將RSbike的所有功能放入restaurant_search.html
    return render(request, 'restaurant_search.html', context)

#PDbike的顯示畫面(初始畫面) 
def PDbike(request):

     #將PDbike的所有功能放入production_search.html
    return render(request, 'production_search.html')

def production_search(request):

    #抓取前端輸入的值
    search_name=request.GET.get("sel_value","")

    
    youbike_information=[]
    
    youbikes_information_districts=[]
    restaurant_information = []


    restaurant_url_districts='https://cuisine-final-project.herokuapp.com:443/api/restaurant/all'
    youbike_url_availability='http://210.61.47.192:80/youbike/api/youbike/station/availability'
    
    youbike_params_districts = {
        'status': 'status',
        'message': 'message',
        'data': 'data'
        }
    restaurant_params_districts =[] 
    
    x = requests.get(youbike_url_availability, params=youbike_params_districts)
    resultss = x.json()

    #從resultss的資料中（type為dictionary），選用key值為data裡的資料，並將值給youbike_data_deals
    youbike_data_deals=resultss['data']
    
    #列result中所有資料，並放入到youbike_data_deals 中
    for result in youbike_data_deals:

        #youbike_data_deals的資料型態為dictionary，固建立一個字典為youbike_data_station，並將result中的資料放入此字典
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
         
         #為了精準搜尋，做字串分割，只取前面的值
        z=youbike_data_station['area'].strip(" Dist.")

        #將處理好的資料，放入youbikes_information_districts
        youbikes_information_districts.append(z) 

        

    r = requests.get(restaurant_url_districts, params=restaurant_params_districts)
    results = r.json()
    #restaurant_data_deals=results['data']
    #youbikes_information.append(youbike_data_deal)
    
    #for result in youbike_data_deal:
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

        pos2=restaurant_data_select['name'].find(search_name)
        
        if pos2>=0 :
            rtable={
                'n':restaurant_data_select['name'],
                'lo':restaurant_data_select['location'],
                'ph':restaurant_data_select['phone'],
                'pro':restaurant_data_select['promotion'],
                'intro':restaurant_data_select['introduction']
                }
                
            for aresultss in youbike_data_deals:
                youbike_data_station = {
                    'id':aresultss['sno'],
                    'name':aresultss['sna'],
                    'area':aresultss['sarea'],
                    'address':aresultss['ar'],
                    'operation':aresultss['act'],
                    'parking':aresultss['tot'],
                    'brrow':aresultss['sbi'],
                    'free':aresultss['bemp'],
                    'update':aresultss['mday']   
                    }
                    
                a=youbike_data_station['area'].strip(" Dist.")
                pos=rtable['lo'].find(a)
                
                if pos>=0:
                    if youbike_data_station['operation']=="1":
                        youbike_data_station['operation']="yes"
                    else:
                        youbike_data_station['operation']="no"
                    
                    youbike_information.append(youbike_data_station) 

            restaurant_information.append(rtable)
        #restaurant_information.append(restaurant_data_select)
       
    context = {
        'youbikes' : youbike_information,
        'restaurant': restaurant_information,
        'Pname':search_name
    }
    
    return render(request, 'production_search.html',context)
