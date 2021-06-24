from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import requests
from collections import OrderedDict as od
# from bs4 import BeautifulSoup
# import datetime


# Create your views here.
def home(request):
    return render(request, 'index.html')


def index(request):

    response = requests.get('https://api.covid19india.org/data.json')
    resp = response.json()

   # India count

    statewise = resp['statewise']

    india = statewise[0]

    total_india = india['confirmed']

    active_india = india['active']

    recovered_india = india['recovered']

    dead_india = india['deaths']

    updated_time_india = india['lastupdatedtime']
    
    state=['Total', 'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'State Unassigned', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    check=[]
    for i in range(len(state)):
        if state[i]=='State Unassigned':
            continue
        check.append([state[i],{'confirmed':statewise[i]['confirmed'],'active':statewise[i]['active'],'recovered':statewise[i]['recovered'],'deaths':statewise[i]['deaths']}])

    context={'name': ['total', 'active', 'recovered', 'dead'],'states':check}

    return render(request, 'covidstat.html', context)

def state(request):
    d={}
    response = requests.get('https://api.covid19india.org/data.json')
    resp = response.json()
    statewise = resp['statewise']
    if request.method== 'POST':
        value=request.POST.get('city')
        i=0
        ind = ''
        for k in statewise:
            if k['state'] == value:
                ind = i
                break
            i = i + 1
        # value=statewise[i]
        value={'confirmed':statewise[i]['confirmed'],'active':statewise[i]['active'],'recovered':statewise[i]['recovered'],'deaths':statewise[i]['deaths']}
        d={'city':value}
    
    return render(request,'state.html',d)

def city(request):
    districtwise = requests.get('https://api.covid19india.org/state_district_wise.json')
    districtwise = districtwise.json()
    tn_districts={}
    if request.method == 'POST':
        value=request.POST.get('city')
        tn_districts = districtwise[value]['districtData']
        t=tn_districts
        key=0
        final={}
        ar=list(t.keys())
        temp=0
        while(len(list(t.keys()))!=0):
            key=0
            ar=list(t.keys())
            temp=0
            for i in range(len(ar)-1):
                for j in range(i+1,len(ar)):
                    #print(t[ar[i]]['confirmed'])
                    if t[ar[i]]['confirmed']>temp:
                        temp=t[ar[i]]['confirmed']
                        key=i
            final[ar[key]]=t[ar[key]]
            del t[ar[key]]
        tn_districts=final
        tn_districts={'tn_districts':tn_districts,'name':value}
    return render(request,'city.html',tn_districts)


# def test(request):

#   response = requests.get('https://api.covid19india.org/data.json')
#   resp = response.json()

#  # India count

#   statewise = resp['statewise']

#   india = statewise[0]

#   total_india = india['confirmed']

#   active_india = india['active']

#   recovered_india = india['recovered']

#   dead_india = india['deaths']

#   updated_time_india = india['lastupdatedtime']

#   #Tamilnadu count

#   i=0
#   ind = ''
#   for k in statewise:
#       if k['state'] == 'Uttar Pradesh':
#           ind = i
#       i = i + 1
#   l=[]
#   for k in statewise:
#     l.append(k['state'])

#   tamilnadu = statewise[ind]

#   total_tamilnadu = tamilnadu['confirmed']

#   active_tamilnadu = tamilnadu['active']

#   recovered_tamilnadu = tamilnadu['recovered']

#   dead_tamilnadu = tamilnadu['deaths']

#  #world count

#   world_response = requests.get('https://www.worldometers.info/coronavirus/')


#   worldsoup = BeautifulSoup(world_response.content, 'html.parser')

#   mydivs = worldsoup.findAll("div", {"class": "maincounter-number"})

#   total_world = mydivs[0].text
#   total_world_death = mydivs[1].text
#   total_world_recovered = mydivs[2].text

#   world_active = worldsoup.findAll("div", {"class": "number-table-main"})

#   world_active_cases = world_active[0].text


#   # Daily cases chart

#   daily_cases = resp['cases_time_series']
#   tot_length = len(daily_cases)

#   last_updated_time = resp['statewise'][0]['lastupdatedtime']

#   today_case = int(resp['statewise'][0]['deltaconfirmed'])

#   sterday_confirmed = int(daily_cases[tot_length-1]['dailyconfirmed'])

#   sterday1_confirmed = int(daily_cases[tot_length-2]['dailyconfirmed'])

#   sterday2_confirmed = int(daily_cases[tot_length-3]['dailyconfirmed'])

#   sterday3_confirmed = int(daily_cases[tot_length-4]['dailyconfirmed'])

#   sterday4_confirmed = int(daily_cases[tot_length-5]['dailyconfirmed'])

#   #--------------------------------------------------------------------------
#   today_death = int(resp['statewise'][0]['deltadeaths'])

#   sterday_death = int(daily_cases[tot_length-1]['dailydeceased'])

#   sterday1_death = int(daily_cases[tot_length-2]['dailydeceased'])

#   sterday2_death = int(daily_cases[tot_length-3]['dailydeceased'])

#   sterday3_death = int(daily_cases[tot_length-4]['dailydeceased'])

#   sterday4_death = int(daily_cases[tot_length-5]['dailydeceased'])

#    #--------------------------------------------------------------------------
#   today_recovered = int(resp['statewise'][0]['deltarecovered'])

#   sterday_recovered = int(daily_cases[tot_length-1]['dailyrecovered'])

#   sterday1_recovered = int(daily_cases[tot_length-2]['dailyrecovered'])

#   sterday2_recovered = int(daily_cases[tot_length-3]['dailyrecovered'])

#   sterday3_recovered = int(daily_cases[tot_length-4]['dailyrecovered'])

#   sterday4_recovered = int(daily_cases[tot_length-5]['dailyrecovered'])

#  #--------------------------------------------------------------------------

#   #statewise daily Changes
#   state=requests.get("https://api.covid19india.org/states_daily.json")
#   s=state.json()
#   s=s['states_daily']
#   tdy_case=int(resp['statewise'][ind]['deltaconfirmed'])
#   y1=s[-3]['tn']
#   y2=s[-6]['tn']
#   y3=s[-9]['tn']
#   y4=s[-12]['tn']
#   y5=s[-15]['tn']

#   print(1,y1)

# # Time calculation

#   tdy = datetime.datetime.today()
#   today = (tdy.strftime("%d")+' '+(tdy.strftime("%B")))

#   ster = datetime.datetime.today() - datetime.timedelta(days=1)
#   yesterday = (ster.strftime("%d")+' '+(ster.strftime("%B")))

#   ster1 = datetime.datetime.today() - datetime.timedelta(days=2)
#   yesterday1 = (ster1.strftime("%d")+' '+(ster1.strftime("%B")))

#   ster2 = datetime.datetime.today() - datetime.timedelta(days=3)
#   yesterday2 = (ster2.strftime("%d")+' '+(ster2.strftime("%B")))

#   ster3 = datetime.datetime.today() - datetime.timedelta(days=4)
#   yesterday3 = (ster3.strftime("%d")+' '+(ster3.strftime("%B")))

#   ster4 = datetime.datetime.today() - datetime.timedelta(days=5)
#   yesterday4 = (ster4.strftime("%d")+' '+(ster4.strftime("%B")))


#   # Tamilnadu district wise

#   districtwise = requests.get('https://api.covid19india.org/state_district_wise.json')

#   districtwise = districtwise.json()

#   tn_districts = districtwise['Uttar Pradesh']['districtData']

#   t=tn_districts
#   key=0
#   final={}
#   ar=list(t.keys())
#   temp=0
#   while(len(list(t.keys()))!=0):
# 	  key=0
# 	  ar=list(t.keys())
# 	  temp=0
# 	  for i in range(len(ar)-1):
# 		  for j in range(i+1,len(ar)):
# 			  #print(t[ar[i]]['confirmed'])
# 			  if t[ar[i]]['confirmed']>temp:
# 				  temp=t[ar[i]]['confirmed']
# 				  key=i
# 	  final[ar[key]]=t[ar[key]]
# 	  del t[ar[key]]
#   tn_districts=final

#   key=5
#   for i in range(0,len(statewise)):
#       for j in range(0,len(statewise)-i-1):
#           if int(statewise[j]['confirmed']) < int(statewise[j+1]['confirmed']) :
#               temp=statewise[j]
#               statewise[j]=statewise[j+1]
#               statewise[j+1]=temp

#   for i in range(0,len(statewise)):
#       if int(statewise[i]['confirmed']) ==0 :
#           key=i
#           break
#   statewise=statewise[:key]

#   return render(request, 'covidstat.html',{'total_india':total_india,'active_india':active_india,'recovered_india':recovered_india,'dead_india':dead_india,'updated_time_india':updated_time_india, 'total_tamilnadu':total_tamilnadu,'active_tamilnadu':active_tamilnadu,'recovered_tamilnadu':recovered_tamilnadu,'dead_tamilnadu':dead_tamilnadu, 'total_world':total_world, 'world_active_cases':world_active_cases, 'total_world_death':total_world_death,'total_world_recovered':total_world_recovered,'today':today,'yesterday':yesterday,'yesterday1':yesterday1,'yesterday2':yesterday2,'yesterday3':yesterday3,'yesterday4':yesterday4,'today_case':today_case,'sterday_confirmed':sterday_confirmed,'sterday1_confirmed':sterday1_confirmed,'sterday2_confirmed':sterday2_confirmed,'sterday3_confirmed':sterday3_confirmed,'sterday4_confirmed':sterday4_confirmed,'tn_districts':tn_districts,
#   'sterday_recovered':sterday_recovered,'sterday1_recovered':sterday1_recovered,'sterday2_recovered':sterday2_recovered,'sterday3_recovered':sterday3_recovered,'sterday4_recovered':sterday4_recovered,'today_recovered':today_recovered,
#   'sterday_death':sterday_death,'sterday1_death':sterday1_death,'sterday2_death':sterday2_death,'sterday3_death':sterday3_death,'sterday4_death':sterday4_death,'today_death':today_death,
#   'tdy_case':tdy_case,'y1':y1,'y2':y2,'y3':y3,'y4':y4,'y5':y5,'statewise':statewise})


    