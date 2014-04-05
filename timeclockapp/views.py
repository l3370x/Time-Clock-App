from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django import forms
from employee.models import *
from timeregistry.models import *
from datetime import datetime

class LoginForm(forms.Form):
  username = forms.CharField(max_length = 100)
  password = forms.CharField(widget = forms.PasswordInput(render_value = False), max_length = 100)

  
def home(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html', {'form':form},
                                  context_instance = RequestContext(request))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render_to_response('login.html', {'form':form},
                                  context_instance = RequestContext(request))

        user = authenticate(username = request.POST['username'],
                            password = request.POST['password'])
        if user is None:
            return render_to_response('login.html',
                                      {'form':form,
                                       'error': 'Invalid username or password'},
                                      context_instance = RequestContext(request))
        login(request, user)
        if user.groups.filter(name = 'Boss').count():
            return bossHome(request)
        if user.is_staff:
            django.contrib.auth.logout(request)
            return render_to_response('login.html',
                                      {'form':form,
                                       'error': 'use carat.bluemoonscience.com/admin for Admin login'},
                                      context_instance = RequestContext(request))
        return redirect('emphome')

@login_required
def user_view(request):
    try:
        theuser = User.objects.get(id = request.user.id)
    except User.DoesNotExist:
        raise Http404
    theemp = Emp.objects.get(user=theuser)
    clockedin = theemp.clockedin
    user_total_week_time = 5.4
    return render(request, 'clock.html', {'theUser':theuser,
                                          'clockedin':clockedin,
                                          'total_time':user_total_week_time})
@login_required
def clockin(request):
    try:
        theuser = User.objects.get(id = request.user.id)
    except User.DoesNotExist:
        raise Http404
    theemp = Emp.objects.get(user=theuser)
    ts = TimeReg(emp=theemp,isclockin=True)
    ts.timestamp = datetime.now()
    ts.save()
    theemp.clockedin = True
    theemp.save()
    return redirect('emphome')

@login_required
def clockout(request):
    try:
        theuser = User.objects.get(id = request.user.id)
    except User.DoesNotExist:
        raise Http404
    theemp = Emp.objects.get(user=theuser)
    ts = TimeReg(emp=theemp,isclockin=False)
    ts.timestamp = datetime.now()
    ts.save()
    theemp.clockedin = False
    theemp.save()
    return redirect('emphome')

@login_required
def boss_view(request):
    try:
        theuser = User.objects.get(id = request.user.id)
    except User.DoesNotExist:
        raise Http404
    clockedin = False
    user_total_week_time = 5.4
    return render(request, 'clock.html', {'theUser':theuser,
                                          'clockedin':clockedin,
                                          'total_time':user_total_week_time})


def forgot(request):
    return render_to_response('forgot.html')

def create(request):
    d = {}
    if request.method == 'GET':
        form = UserForm()
        d['form'] = form
        return render_to_response('new.html', d, context_instance = RequestContext(request))

    if request.method == 'POST':
        form = UserForm(request.POST)
        d['form'] = form
        if not form.is_valid():
            return render_to_response('new.html', d, context_instance = RequestContext(request))

        try:
            u = User.objects.get(username = request.POST['username'])
            d['error'] = 'Username already taken'
            return render_to_response('new.html', d, context_instance = RequestContext(request))
        except User.DoesNotExist:
            pass

        if request.POST['password'] != request.POST['confirm']:
            d['error'] = 'Passwords must match'
            return render_to_response('new.html', d, context_instance = RequestContext(request))

        userO = User.objects.create_user(request.POST['username'],
                                        request.POST['email'],
                                        request.POST['password'])
        userO.save()
        person = Emp.objects.create(user = userO,
                                    first_name = request.POST['first_name'],
                                    last_name = request.POST['last_name'],
                                    email = request.POST['email'],
                                    phone = request.POST['phone'])


        return redirect('home')