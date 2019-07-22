#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, HttpResponse

from .models import UserType, Barbershop, BarbershopSchedule

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils.translation import gettext as _

from datetime import datetime
from dateutil import parser
from django.utils import timezone
from .forms import BarberUserSettingsForm, EmployeeForm
from django.forms import formset_factory

@login_required
def landing(request):
    user = request.user
    # TODO filter barbershops by distance

    if 'barber' == str(user.user_type):
        try:
            barbershop = Barbershop.objects.get(owner=user)
            data = {
                'barbershop': barbershop
            }
        except Barbershop.DoesNotExist:
            return redirect('user-settings')


    elif 'customer' == str(user.user_type):
        barbershops = Barbershop.objects.all()
        data = {'barbershops': barbershops}

    
    return render(request, str(user.user_type) + '/dashboard.html',
                  {'data': data, 'user': user})

@login_required
def user_settings(request):
    user = request.user

    def _init_forms_and_extra(extra=None):
        try:
            barbershop = Barbershop.objects.get(owner=user)
            form = BarberUserSettingsForm(
                initial={
                    'barbershop_name':barbershop.name,
                    'address_description':barbershop.address.description
                }
            )
            if barbershop.employees.exists():
                #TODO optimize this
                extra = 0 if extra is None else extra
                FormSet = formset_factory(EmployeeForm, extra=extra)
                formset = FormSet(initial=[{'title':emp.title, 'name': emp.name, 'surname':emp.surname} for emp in barbershop.employees.all()])
            else:
                extra = 1 if extra is None else extra
                formset = formset_factory(EmployeeForm, extra=extra)
                
        except Barbershop.DoesNotExist:
            form = BarberUserSettingsForm()
            extra = 1 if extra is None else extra
            formset = formset_factory(EmployeeForm, extra=extra)
        return form, formset, extra

    if 'barber' == str(user.user_type):
        if request.method == 'POST':
            if request.POST['action'] == "+":
                form, formset, extra = _init_forms_and_extra(int(float(request.POST['extra'])) + 1)
            else:
                extra = int(float(request.POST['extra']))
                form = BarberUserSettingsForm(request.POST)
                formset = formset_factory(EmployeeForm, extra=extra)(request.POST)

                if form.is_valid() and formset.is_valid():
                    if request.POST['action'] == "Create":
                        for form_employee in formset:
                            if not 'delete' in form_employee.cleaned_data:
                                # create data
                                barbershop = form.save(user)
                                form_employee.save(barbershop)
                    elif request.POST['action'] == "Edit":
                        for form_employee in formset:
                            if 'delete' in form_employee.cleaned_data and form_employee.cleaned_data['delete']:
                                pass
                                # delete data
                            else:
                                pass
                                # create data
                    
            return render(request, str(user.user_type) + '/settings.html', {'user': user, 'form': form, 'formset':formset, 'extra': extra})
        
        form, formset, extra = _init_forms_and_extra()

        return render(request, str(user.user_type) + '/settings.html', {'user': user, 'form': form, 'formset':formset, 'extra': extra})


    return render(request, str(user.user_type) + '/settings.html', {'data': data})

@login_required
def map(request):
    user = request.user

    data = {'de': 'de'}

    return render(request, str(user.user_type) + '/map.html', {'data': data})

@login_required
def barbershop(request, barbershop_slug):
    print(barbershop_slug)
    user = request.user

    try:
        barbershop = Barbershop.objects.get(slug=barbershop_slug)
    except:
        return HttpResponseNotFound("hello")    

    # barbershop.employees = list(barbershop.employees.all().values())
    print(list(barbershop.schedules.all().values()))
    now = timezone.localtime(timezone.now())

    data = {
        'barbershop': {
            'name': barbershop.name,
            'id': barbershop.id,
            'services': list(barbershop.services.all().values()),
            'employees': list(barbershop.employees.all().values()),
            'schedules': list(barbershop.schedules.filter(start_time__day=now.day).values(
                'start_time__hour', 'start_time__minute', 'end_time__hour', 'end_time__minute', 'assigned_employee'
                ))
        }
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    print(data)
    return render(request, str(user.user_type) + '/barbershop.html', data)

@login_required
def schedule_customer(request):
    user = request.user

    start_time = parser.parse(request.POST['startTime'])
    end_time = parser.parse(request.POST['endTime'])
    services = request.POST['services'].split(',')
    employee_id = request.POST['employeeID']
    barbershop_id = request.POST['barbershopID']
    print(start_time, "wololo")

    print(services)
    try:
        BarbershopSchedule.objects.create(
            start_time=start_time,
            end_time=end_time,
            services=services,
            barbershop_id=barbershop_id,
            assigned_employee_id=employee_id,
            customer=request.user
        )
    except Exception as err:
        raise err
    return redirect("landing")
