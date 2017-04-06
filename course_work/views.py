from django.shortcuts import render, redirect
from course_work.models import Driver
from .forms import IndexForm
from django.core.exceptions import ObjectDoesNotExist


def passenger_list(request):
    return render(request, 'course_work/passenger_list.html', {})

def index(request):
    if request.method == "POST":
        form = IndexForm(request.POST)
        if form.is_valid():
            login = request.POST.get('login', )
            password = request.POST.get('password', "")
            print(login, password)
            try:
                d = Driver.objects.filter(login__exact=login).filter(password__exact=password).get()
                return redirect('workspace')
            except ObjectDoesNotExist:
                return redirect('index')

    else:
        form = IndexForm()

    return render(request, 'course_work/index.html', {'form': form})

def workspace(request):
    return render(request, 'course_work/workspace.html', {})