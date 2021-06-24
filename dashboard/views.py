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
    check={}
    for i in range(1,len(state)):
        check[state[i]] = {'total':statewise[i]['confirmed'],'active':statewise[i]['active'],'recovered':statewise[i]['recovered'],'death':statewise[i]['deaths']}
        
    context={'name': ['total', 'active', 'recovered', 'dead'],'states':check}

    return render(request, 'covidstat.html', context)
