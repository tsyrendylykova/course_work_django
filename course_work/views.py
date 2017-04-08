from django.shortcuts import render, redirect, get_object_or_404
from course_work.models import Driver, Location
from course_work.search_engine import find_passengers
from .forms import IndexForm, DriverForm
from django.core.exceptions import ObjectDoesNotExist


def passenger_list(request):
    return render(request, 'course_work/passenger_list.html', {})

def index(request):
    if request.method == "POST":
        form = IndexForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            try:
                d = Driver.objects.filter(login__exact=login).filter(password__exact=password).get()
                return redirect('workspace')
            except ObjectDoesNotExist:
                return redirect('index')

    else:
        form = IndexForm()

    return render(request, 'course_work/index.html', {'form': form})


def workspace(request):
    if request.method == "POST":
        form = DriverForm(data=request.POST)
        if form.is_valid():
            start_point = form.cleaned_data.get('start_point')
            end_point = form.cleaned_data.get('end_point')
            date = form.cleaned_data.get('date')
            number_of_free_seats = form.cleaned_data.get('number_of_free_seats')

            print(start_point, end_point, date, number_of_free_seats)

            passengers_result = find_passengers(start_point, end_point, date, number_of_free_seats)

            return render(request, 'course_work/workspace.html', {'form': form, 'passengers_list': passengers_result})
    else:
        form = DriverForm()
    return render(request, 'course_work/workspace.html', {'form': form})
