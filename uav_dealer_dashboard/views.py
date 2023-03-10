from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from uav_dealer_dashboard.models import *
from customer_dashboard.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'uav_dealer_login.html')
    else:
        return render(request, 'uav_dealer_home_page.html')

def login(request):
    return render(request, 'uav_dealer_login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'uav_dealer_home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            uav_dealer = uavDealer.objects.get(uav_dealer = user)
        except:
            uav_dealer = None
        if uav_dealer is not None:
            auth.login(request, user)
            return render(request, 'uav_dealer_home_page.html')
        else:
            return render(request, 'uav_dealer_login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'uav_dealer_login.html')

def register(request):
    return render(request, 'uav_dealer_register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']

    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'uav_dealer_registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        uav_dealer = uavDealer(uav_dealer = user, mobile = mobile, area=area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        uav_dealer = uavDealer(uav_dealer = user, mobile = mobile, area=area)
    uav_dealer.save()
    return render(request, 'uav_dealer_registered.html')

@login_required
def add_vehicle(request):
    uav_name = request.POST['uav_name']
    color = request.POST['color']
    cd = uavDealer.objects.get(uav_dealer=request.user)
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    description = request.POST['description']
    capacity = request.POST['capacity']
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        uav = Vehicles(uav_name=uav_name, color=color, dealer=cd, area = area, description = description, capacity=capacity)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        uav = Vehicles(uav_name=uav_name, color=color, dealer=cd, area = area,description=description, capacity=capacity)
    uav.save()
    return render(request, 'uav_dealer_vehicle_added.html')

@login_required
def manage_vehicles(request):
    username = request.user
    user = User.objects.get(username = username)
    uav_dealer = uavDealer.objects.get(uav_dealer = user)
    vehicle_list = []
    vehicles = Vehicles.objects.filter(dealer = uav_dealer)
    for v in vehicles:
        vehicle_list.append(v)
    return render(request, 'uav_dealer_manage.html', {'vehicle_list':vehicle_list})

@login_required
def order_list(request):
    username = request.user
    user = User.objects.get(username = username)
    uav_dealer = uavDealer.objects.get(uav_dealer = user)
    orders = Orders.objects.filter(car_dealer = uav_dealer)
    order_list = []
    for o in orders:
        if o.is_complete == False:
            order_list.append(o)
    return render(request, 'uav_dealer_order_list.html', {'order_list':order_list})

@login_required
def complete(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    order.is_complete = True
    order.save()
    vehicle.is_available = True
    vehicle.save()
    return HttpResponseRedirect('/uav_dealer_dashboard/order_list/')


@login_required
def history(request):
    user = User.objects.get(username = request.user)
    uav_dealer = uavDealer.objects.get(uav_dealer = user)
    orders = Orders.objects.filter(uav_dealer = uav_dealer)
    order_list = []
    for o in orders:
        order_list.append(o)
    return render(request, 'uav_dealer_history.html', {'wallet':uav_dealer.wallet, 'order_list':order_list})

@login_required
def delete(request):
    veh_id = request.POST['id']
    vehicle = Vehicles.objects.get(id = veh_id)
    vehicle.delete()
    return HttpResponseRedirect('/uav_dealer_dashboard/manage_vehicles/')
