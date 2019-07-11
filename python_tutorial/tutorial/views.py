import time
import xlrd
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import get_signin_url, get_token_from_code, get_access_token
from tutorial.outlookservice import get_me,get_my_messages,get_my_events
from tutorial.models import *
from datetime import datetime

# Create your views here.

def signup_view(request):
  post = request.POST
  user = User.objects.create_user(post['username'],post['email'],post['password'])
  user.save()
  return render(request,'tutorial/layout.html')

def login_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request,username=username,password=password)
  if user is not None:
    login(user)
  else:
    pass
  return render(request,'tutorial/layout.html')

def home(request):
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = { 'signin_url': sign_in_url }
  return render(request, 'tutorial/home.html', context)

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']

  # expires_in is in seconds
  # Get current timestamp (seconds since Unix Epoch) and
  # add expires_in to get expiration time
  # Subtract 5 minutes to allow for clock differences
  expiration = int(time.time()) + expires_in - 300

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  return HttpResponseRedirect(reverse('tutorial:mail'))

def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    messages = get_my_messages(access_token)
    context = { 'messages': messages['value'] }
    return render(request, 'tutorial/mail.html', context)

def events(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    events = get_my_events(access_token)
    context = { 'events': events['value'] }
    return render(request, 'tutorial/events.html', context)

def book_a_room(request):
  user = request.user
  data = request.POST
  print('karlo')
  print(data['room_name'])
  room = RoomInfo.objects.get(name=data['room_name'])
  start_time = datetime.fromtimestamp(int(data['start_time'][:-3]))
  end_time = datetime.fromtimestamp(int(data['end_time'][:-3]))
  booked_room = Bookings(user=user,room_name=room,start_time=start_time,end_time=end_time)
  booked_room.save()
  return render(request,'tutorial/layout.html')

def fillData(path):
  room_sheets = xlrd.open_workbook(path)
  first_sheet = room_sheets.sheet_by_index(0)
  for i in range(2,63):
    location = ''
    for j in range(0,3):
      if first_sheet.cell(i,j).value=='Cherry hills ':
        location += ' '
      location += first_sheet.cell(i,j).value 
    # print(location)
    new_room = RoomInfo(name = first_sheet.cell(i,3).value, total_seats = 8, location = location,
                       projector_status = True, comm_status = True)
    new_room.save()

def check_availability(request):
  post = request.POST
  # print ('karlo acche se')
  #'start': ['2019-07-12 11:50'], 'duration': ['39']
  user = request.user
  start_time = epochs(post['start'])
  end_time = start_time + int(post['duration'])*60
  booked_rooms = Bookings.objects.all()
  all_rooms = RoomInfo.objects.all()
  available_rooms = []
  s = set()
  #cnt=0
  for i in booked_rooms:
    # if cnt == 0:
    #   print("tm:"+str(i.start_time.timestamp()))
    if i.user==user and (i.start_time.timestamp()<=start_time<=i.end_time.timestamp() or i.start_time.timestamp()<=end_time<=i.end_time.timestamp()):
      s.add(i.room_name)
  for i in all_rooms:
    if i not in s:
      available_rooms.append(i)
  return render(request,'tutorial/timeformat.html',{'available_rooms':all_rooms,'start':start_time,'end':end_time})

def epochs(tm):
  stArr=tm.split(' ')
  stArr2=list(map(int,stArr[0].split('-')))
  stArr3=list(map(int,stArr[1].split(':')))

  start_time = datetime(stArr2[0],stArr2[1],stArr2[2],stArr3[0],stArr3[1]).timestamp()
  return start_time

