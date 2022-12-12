import json
import threading
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth import logout as logout_admin
from django.contrib import auth

class MyLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user'))
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'data' in kwargs.keys():
            if User.objects.filter(mobile = kwargs['data']['username']).exists():
                kwargs['data']._mutable=True
                kwargs['data']['username'] = User.objects.get(mobile = kwargs['data']['username']).email                
                kwargs['data']._mutable=False
        kwargs["request"] = self.request
        return kwargs


def Register(request):
    if request.method == 'POST':
        form=RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            emai_send = threading.Thread(
                target=send_an_email, args=['Welcome mail', 'Welcome to the Bombay softwares.',user])
            emai_send.start()
            auth.login(request,user)
            return redirect('user')
        else:
            return render(request, 'registration/register.html', {'form': form}) 

    return render(request,'registration/register.html',{'form':RegisterUserForm()})


@login_required(login_url='/login/')
def Logout(request):
    logout_admin(request)
    messages.success(request, 'You are successfully logout.')
    return redirect('login')

def get_proper_elided_page_range(p, number, on_each_side=3, on_ends=2):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side, on_ends=on_ends)

@login_required(login_url='/login/')
def UserListing(request):
    paginator = Paginator(User.objects.all(), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj_number = page_obj.number
    page_obj_has_previous = page_obj.has_previous()
    page_obj_has_next = page_obj.has_next()
    page_list = []

    if page_obj_has_previous:
        previous_page_number = page_obj.previous_page_number()
    else:
        previous_page_number = ''

    if page_obj_has_next:
        page_obj_next_page_number = page_obj.next_page_number()
    else:
        page_obj_next_page_number = ''

    for row in get_proper_elided_page_range(page_obj.paginator, page_obj.number):
        page_list.append(row)
    pagination_data = [{
        'page_obj_next_page_number': page_obj_next_page_number,
        'previous_page_number': previous_page_number,
        'page_obj_has_next': page_obj_has_next,
        'page_obj_has_previous': page_obj_has_previous,
        'page_list': page_list,
        'page_obj_number': page_obj_number
    },]

    return render(request,'user.html',{'data':page_obj,'pagination_data': json.dumps(pagination_data)})

@login_required(login_url='/login/')
def Update_password_show(request):
    return render(request, 'change_password.html')

@login_required(login_url='/login/')
def Update_password_validation(request):
    error = "0"
    Email = (request.GET.get('Email'))
    Current_Password = (request.GET.get('Current_Password'))
    New_Passsword = (request.GET.get('New_Passsword'))
    Confirm_New_Passsword = (request.GET.get('Confirm_New_Passsword'))
    if Current_Password == "" or New_Passsword == "" or Confirm_New_Passsword == "":
        error = 3
    else:
        if New_Passsword == Confirm_New_Passsword:
            user = auth.authenticate(email=Email, password=Current_Password)
            if user is None:
                error = "1"
            elif len(New_Passsword)<8:
                error = "4"
        else:
            error = "2"
    data = {'response': error}
    return JsonResponse(data)

@login_required(login_url='/login/')
def Update_password_save(request):
    if(request.method == "POST"):
        Email = request.POST['email']
        Current_Password = request.POST['current_password']
        new_password = request.POST['new_password']
        user = auth.authenticate(email=Email, password=Current_Password)
        if user is not None:
            user.set_password(new_password)
            emai_send = threading.Thread(
                target=send_an_email, args=['Password update', 'Password update successfuly.',user.email])
            emai_send.start()
            user.save()
    messages.success(request, 'Password Update Successfully.')
    return redirect('user')

@login_required(login_url='/login/')
def EditProfile(request):
    if request.method == 'POST':
        form=RegisterUserForm(request.POST, instance=User.objects.get(pk=request.user.pk))
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit profile successfully edit')
            return redirect('user')
        else:
            return render(request, 'profile-edit.html', {'form': form}) 
    return render(request,'profile-edit.html',{'form':RegisterUserForm(instance=User.objects.get(pk=request.user.pk))})

from django.core.mail import send_mail
def send_an_email(subject, body,email):
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )