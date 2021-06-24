from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import requests
# from bs4 import BeautifulSoup
# import datetime


# Create your views here.

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

    state = ['Total', 'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
             'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'State Unassigned', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    check = []
    for i in range(len(state)):
        if state[i] == 'State Unassigned':
            continue
        check.append([state[i], {'confirmed': statewise[i]['confirmed'], 'active':statewise[i]
                                 ['active'], 'recovered':statewise[i]['recovered'], 'deaths':statewise[i]['deaths']}])

    context = {'name': ['total', 'active',
                        'recovered', 'dead'], 'states': check}

    return render(request, 'covidstat.html', context)


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
                        'recovered', 'dead'], 'states': check, 'confirmed': total_india, 'actve': active_india, 'recovered': recovered_india, 'deaths': dead_india}

    return render(request, 'index.html', context,)
