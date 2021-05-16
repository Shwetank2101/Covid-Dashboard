from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import requests



# Create your views here.
# def index(request):
# 	return render(request,'index.html')

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

  #Uttar Pradesh count

  i=0
  ind = ''
  for k in statewise:
      if k['state'] == 'Uttar Pradesh':
          ind = i
      i = i + 1

  uttarpradesh = statewise[ind]

  total_uttarpradesh = {'total':uttarpradesh['confirmed']}

  active_uttarpradesh = {'active':uttarpradesh['active']}

  recovered_uttarpradesh = {'recovered':uttarpradesh['recovered']}

  dead_uttarpradesh = {'dead':uttarpradesh['deaths']}
  context={'a':[total_uttarpradesh,active_uttarpradesh,recovered_uttarpradesh,dead_uttarpradesh],'name':['total','active','recovered','dead']}

  return render(request,'covidstat.html',context)