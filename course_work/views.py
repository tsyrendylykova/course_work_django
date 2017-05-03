import random

from django.shortcuts import render, redirect
from course_work.models import Driver
from course_work.search_engine import start_v, dijkstra, get_graph, find_N_optimal_passengers
from .forms import IndexForm, DriverForm
from django.core.exceptions import ObjectDoesNotExist


def passenger_list(request):
    return render(request, 'course_work/passenger_list.html', {})

def login(request):
    if request.method == "POST":
        form = IndexForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            try:
                d = Driver.objects.filter(login__exact=login).filter(password__exact=password).get()
                return redirect('index')
            except ObjectDoesNotExist:
                return redirect('login')

    else:
        form = IndexForm()

    return render(request, 'course_work/login.html', {'form': form})


def index(request):
    if request.method == "POST":
        form = DriverForm(data=request.POST)
        if form.is_valid():
            start_point = form.cleaned_data.get('start_point')
            end_point = form.cleaned_data.get('end_point')
            date = form.cleaned_data.get('date')
            number_of_free_seats = form.cleaned_data.get('number_of_free_seats')

            current_point, end, route, visited, distances, predecessors = start_v(start_point.name, end_point.name)
            G = get_graph()
            dijkstra(G, current_point, end, route, visited, distances, predecessors)
            print(route)
            passengers_result = find_N_optimal_passengers(start_point, end_point, date, number_of_free_seats)
            return render(request, 'course_work/index.html', {'form': form, 'passengers_list': passengers_result, 'route': route})
    else:
        form = DriverForm()
    return render(request, 'course_work/index.html', {'form': form})
