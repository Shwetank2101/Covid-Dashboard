from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import requests
from collections import OrderedDict as od


# Create your views here.
def home(request):
    return render(request, 'index.html')

# def covid(request):
# 	# data=requests.get('https://api.covid19api.com/countries').json
# 	data=states.getdata()

# 	print(data)
# 	context ={'data':data}
# 	return render(request,'covidstat.html',context)


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

    context={'name': ['total', 'active', 'recovered', 'dead'],'states':check,'city':uttarpradesh_district,'statewise':tn_districts}

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
    d={}
    if request.method== 'POST':
        value=request.POST.get('city')
        districtwise = requests.get('https://api.covid19india.org/state_district_wise.json')
        districtwise = districtwise.json()
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
        value=tn_districts
        d={'city':value}
    
    
    return render(request,'city.html',d)



    