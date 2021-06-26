from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import requests
import pandas as pd
import io
import datetime
from datetime import date
from datetime import timedelta

# Create your views here.

def state(request):
    d = {}
    response = requests.get('https://api.covid19india.org/data.json')
    resp = response.json()
    statewise = resp['statewise']
    if request.method == 'POST':
        value = request.POST.get('city')
        i = 0
        ind = ''
        for k in statewise:
            if k['state'] == value:
                ind = i
                break
            i = i + 1
        # value=statewise[i]
        value = {'confirmed': statewise[i]['confirmed'], 'active': statewise[i]['active'],
                 'recovered': statewise[i]['recovered'], 'deaths': statewise[i]['deaths']}
        d = {'city': value}

    return render(request, 'index.html', d)


def city(request):
    districtwise = requests.get(
        'https://api.covid19india.org/state_district_wise.json')
    districtwise = districtwise.json()
    tn_districts = {}
    if request.method == 'POST':
        value = request.POST.get('city')
        tn_districts = districtwise[value]['districtData']
        t = tn_districts
        key = 0
        final = {}
        ar = list(t.keys())
        temp = 0
        while(len(list(t.keys())) != 0):
            key = 0
            ar = list(t.keys())
            temp = 0
            for i in range(len(ar)-1):
                for j in range(i+1, len(ar)):
                    # print(t[ar[i]]['confirmed'])
                    if t[ar[i]]['confirmed'] > temp:
                        temp = t[ar[i]]['confirmed']
                        key = i
            final[ar[key]] = t[ar[key]]
            del t[ar[key]]
        tn_districts = final
        tn_districts = {'tn_districts': tn_districts, 'name': value}
    return render(request, 'city.html', tn_districts)

def vaccination(request):
    req = requests.get(
        "https://api.rootnet.in/covid19-in/stats/testing/history"
    )
    req = req.json()
    req=req['data']
    day1=req[-1]['totalSamplesTested']
    day2=req[-2]['totalSamplesTested']
    today=day1-day2


    vaccine=requests.get(
            "http://api.covid19india.org/csv/latest/vaccine_doses_statewise_v2.csv"
        ).content
    vaccine=pd.read_csv(io.StringIO(vaccine.decode('utf-8')))

    firstdose={}
    seconddose={}
    state = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
                'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
        
    for i in range(1,39):
        firstdose[vaccine.iloc[-i]['State']]=vaccine.iloc[-i]['First Dose Administered']-vaccine.iloc[-i-38]['First Dose Administered'] 
        seconddose[vaccine.iloc[-i]['State']]=vaccine.iloc[-i]['Second Dose Administered']-vaccine.iloc[-i-38]['Second Dose Administered'] 
  
    context=[]
    for i in state:
        context.append({'state':i,'first':firstdose[i],'second':seconddose[i]})
    indiafirst=firstdose['Total']
    indiasecond=seconddose['Total']
    
    print(indiafirst)

    context={'today':today,'day':req[-1]['day'],'vaccine':vaccine,'state':state,'context':context,'date':date,'indiafirst':indiafirst,'indiasecond':indiasecond}
    return render(request, 'vaccination.html', context)
    

def home(request):

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


    state = ['Total', 'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
             'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'State Unassigned', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    check = []

    for i in range(len(state)):
        if state[i] == 'State Unassigned':
            continue
        check.append([state[i], {'confirmed': statewise[i]['confirmed'], 'active':statewise[i]
                                 ['active'], 'recovered':statewise[i]['recovered'], 'deaths':statewise[i]['deaths']}])

    context = {'name': ['total', 'active',
                        'recovered', 'dead'], 'states': check, 'confirmed': total_india, 'active': active_india, 'recovered': recovered_india, 'deaths': dead_india}


    #state
    response = requests.get('https://api.covid19india.org/data.json')
    resp = response.json()
    statewise = resp['statewise']

    #city
    districtwise = requests.get('https://api.covid19india.org/state_district_wise.json')
    districtwise = districtwise.json()
    tn_districts = {}
    if request.method == 'POST':
        value = request.POST.get('city')
        value1 = value
        i = 0
        ind = ''
        for k in statewise:
            if k['state'] == value:
                ind = i
                break
            i = i + 1
        # value=statewise[i]
        value = {'confirmed': statewise[i]['confirmed'], 'active': statewise[i]['active'],
                 'recovered': statewise[i]['recovered'], 'deaths': statewise[i]['deaths']}
        context['city'] = value

        
        tn_districts = districtwise[value1]['districtData']
        t = tn_districts
        key = 0
        final = {}
        ar = list(t.keys())
        temp = 0
        while(len(list(t.keys())) != 0):
            key = 0
            ar = list(t.keys())
            temp = 0
            for i in range(len(ar)-1):
                for j in range(i+1, len(ar)):
                    # print(t[ar[i]]['confirmed'])
                    if t[ar[i]]['confirmed'] > temp:
                        temp = t[ar[i]]['confirmed']
                        key = i
            final[ar[key]] = t[ar[key]]
            del t[ar[key]]
        tn_districts = final
        context['tn_districts']=tn_districts
        context['name1']=value1

        

    req = requests.get(
        "https://api.rootnet.in/covid19-in/stats/testing/history"
    )
    req = req.json()
    req=req['data']
    day1=req[-1]['totalSamplesTested']
    day2=req[-2]['totalSamplesTested']
    today=day1-day2


    vaccine=requests.get(
            "http://api.covid19india.org/csv/latest/vaccine_doses_statewise_v2.csv"
        ).content
    vaccine=pd.read_csv(io.StringIO(vaccine.decode('utf-8')))

    firstdose={}
    seconddose={}
    state = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
                'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
        
    for i in range(1,39):
        firstdose[vaccine.iloc[-i]['State']]=vaccine.iloc[-i]['First Dose Administered']-vaccine.iloc[-i-38]['First Dose Administered'] 
        seconddose[vaccine.iloc[-i]['State']]=vaccine.iloc[-i]['Second Dose Administered']-vaccine.iloc[-i-38]['Second Dose Administered'] 
  
    context1=[]
    for i in state:
        context1.append({'state':i,'first':firstdose[i],'second':seconddose[i]})
    indiafirst=firstdose['Total']
    indiasecond=seconddose['Total']
    
    print(indiafirst)

    #context={'today':today,'day':req[-1]['day'],'vaccine':vaccine,'state':state,'context':context1,'date':date,'indiafirst':indiafirst,'indiasecond':indiasecond}

    context['today']=today
    context['day']=req[-1]['day']
    context['vaccine']=vaccine
    context['state']=state
    context['context']=context1
    context['date']=date
    context['indiafirst']=indiafirst
    context['indiasecond']=indiasecond

    return render(request, 'index.html', context,)


def covid(request):

    response = requests.get('https://api.covid19india.org/data.json')
    resp = response.json()

        # Daily cases chart
    daily_cases = resp['cases_time_series']
    tot_length = len(daily_cases)

    last_updated_time = resp['statewise'][0]['lastupdatedtime']

    today_case = int(resp['statewise'][0]['deltaconfirmed'])

    sterday_confirmed = int(daily_cases[tot_length-1]['dailyconfirmed'])

    sterday1_confirmed = int(daily_cases[tot_length-2]['dailyconfirmed'])

    sterday2_confirmed = int(daily_cases[tot_length-3]['dailyconfirmed'])

    sterday3_confirmed = int(daily_cases[tot_length-4]['dailyconfirmed'])

    sterday4_confirmed = int(daily_cases[tot_length-5]['dailyconfirmed'])

    sterday5_confirmed = int(daily_cases[tot_length-6]['dailyconfirmed'])

    sterday6_confirmed = int(daily_cases[tot_length-6]['dailyconfirmed'])

    sterday7_confirmed = int(daily_cases[tot_length-7]['dailyconfirmed'])

    sterday8_confirmed = int(daily_cases[tot_length-8]['dailyconfirmed'])

    #--------------------------------------------------------------------------
    today_death = int(resp['statewise'][0]['deltadeaths'])

    sterday_death = int(daily_cases[tot_length-1]['dailydeceased'])

    sterday1_death = int(daily_cases[tot_length-2]['dailydeceased'])

    sterday2_death = int(daily_cases[tot_length-3]['dailydeceased'])

    sterday3_death = int(daily_cases[tot_length-4]['dailydeceased'])

    sterday4_death = int(daily_cases[tot_length-5]['dailydeceased'])

    sterday5_death = int(daily_cases[tot_length-6]['dailydeceased'])

    sterday6_death = int(daily_cases[tot_length-7]['dailydeceased'])

    sterday7_death = int(daily_cases[tot_length-8]['dailydeceased'])

    sterday8_death = int(daily_cases[tot_length-9]['dailydeceased'])

    #--------------------------------------------------------------------------

    today_recovered = int(resp['statewise'][0]['deltarecovered'])

    sterday_recovered = int(daily_cases[tot_length-1]['dailyrecovered'])

    sterday1_recovered = int(daily_cases[tot_length-2]['dailyrecovered'])

    sterday2_recovered = int(daily_cases[tot_length-3]['dailyrecovered'])

    sterday3_recovered = int(daily_cases[tot_length-4]['dailyrecovered'])

    sterday4_recovered = int(daily_cases[tot_length-5]['dailyrecovered'])

    sterday5_recovered = int(daily_cases[tot_length-6]['dailyrecovered'])

    sterday6_recovered = int(daily_cases[tot_length-7]['dailyrecovered'])

    sterday7_recovered = int(daily_cases[tot_length-8]['dailyrecovered'])

    sterday8_recovered = int(daily_cases[tot_length-9]['dailyrecovered'])

    #--------------------------------------------------------------------------

    # Time calculation

    tdy = datetime.datetime.today()
    today = (tdy.strftime("%d")+' '+(tdy.strftime("%B")))

    ster = datetime.datetime.today() - datetime.timedelta(days=1)
    yesterday = (ster.strftime("%d")+' '+(ster.strftime("%B")))

    ster1 = datetime.datetime.today() - datetime.timedelta(days=2)
    yesterday1 = (ster1.strftime("%d")+' '+(ster1.strftime("%B")))

    ster2 = datetime.datetime.today() - datetime.timedelta(days=3)
    yesterday2 = (ster2.strftime("%d")+' '+(ster2.strftime("%B")))

    ster3 = datetime.datetime.today() - datetime.timedelta(days=4)
    yesterday3 = (ster3.strftime("%d")+' '+(ster3.strftime("%B")))

    ster4 = datetime.datetime.today() - datetime.timedelta(days=5)
    yesterday4 = (ster4.strftime("%d")+' '+(ster4.strftime("%B")))
    
    ster5 = datetime.datetime.today() - datetime.timedelta(days=6)
    yesterday5 = (ster5.strftime("%d")+' '+(ster5.strftime("%B")))

    ster6 = datetime.datetime.today() - datetime.timedelta(days=7)
    yesterday6 = (ster6.strftime("%d")+' '+(ster6.strftime("%B")))

    ster7 = datetime.datetime.today() - datetime.timedelta(days=8)
    yesterday7 = (ster7.strftime("%d")+' '+(ster7.strftime("%B")))

    ster8 = datetime.datetime.today() - datetime.timedelta(days=9)
    yesterday8 = (ster8.strftime("%d")+' '+(ster8.strftime("%B")))


    context={'sterday_confirmed':sterday_confirmed,'sterday1_confirmed':sterday1_confirmed,
    'sterday2_confirmed':sterday2_confirmed,'sterday3_confirmed':sterday3_confirmed,
    'sterday4_confirmed':sterday4_confirmed,'sterday5_confirmed':sterday5_confirmed,
    'sterday6_confirmed':sterday6_confirmed,'sterday7_confirmed':sterday7_confirmed,
    'sterday8_confirmed':sterday8_confirmed,
    'sterday_recovered':sterday_recovered,
    'sterday1_recovered':sterday1_recovered,'sterday2_recovered':sterday2_recovered,
    'sterday3_recovered':sterday3_recovered,'sterday4_recovered':sterday4_recovered,
    'sterday5_recovered':sterday5_recovered,'sterday6_recovered':sterday6_recovered,
    'sterday7_recovered':sterday7_recovered,'sterday8_recovered':sterday8_recovered,
    'sterday_death':sterday_death,
    'sterday1_death':sterday1_death,'sterday2_death':sterday2_death,
    'sterday3_death':sterday3_death,'sterday4_death':sterday4_death,
    'sterday5_death':sterday5_death,'sterday6_death':sterday6_death,
    'sterday7_death':sterday7_death,'sterday8_death':sterday8_death,
    'yesterday':yesterday,'yesterday1':yesterday1,'yesterday2':yesterday2,
    'yesterday3':yesterday3,'yesterday4':yesterday4,'yesterday5':yesterday5
    ,'yesterday6':yesterday6,'yesterday7':yesterday7,'yesterday8':yesterday8}


    return render(request,'covid.html',context)