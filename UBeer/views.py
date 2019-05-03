from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as login_user, logout
from UBeer.models import Trips, Riders, Establishments
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


@csrf_exempt
def payment_done(request):
    return render(request, 'rider/confirm.html', {'message': "Your order was successfully submitted"})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'rider/confirm.html', {'message': "There was an error, please retry or try later"})


def payment_process(request):
    host = "6c4d5445.ngrok.io"
    paypal_dict = {
        "business": "false.namebad-facilitator@gmail.com",
        "amount": "10.00",
        "item_name": "name of the item",
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return": 'http://{}{}'.format(host, reverse('done')),
        "cancel_return": 'http://{}{}'.format(host, reverse('canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render_to_response("payment/payment.html", {'form': form})


def login(request):
    context = {
        'data': {},
        'errors': [],
    }

    Group .objects.get_or_create(name='rider')
    Group.objects.get_or_create(name='establishment')

    if request.method == 'POST':
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                request.session.set_expiry(86400)
                login_user(request, user)

                if user.groups.filter(name='rider').exists():
                    return HttpResponseRedirect('/riderHome')
                if user.groups.filter(name='establishment').exists():
                    return HttpResponseRedirect('/establishmentHome')
        else:
            context['errors'].append("The username or password is incorrect.")

    return render(request, "login.html", context)


def signup(request):
    context = {
        'data': {},
        'errors': [],
    }

    Group.objects.get_or_create(name='rider')
    Group.objects.get_or_create(name='establishment')

    if request.method == 'POST':
        data = request.POST
        username = data.get('username', '')
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        password = data.get('password', '')
        email = data.get('email', '')

        if User.objects.filter(username=username).exists():
            context['errors'].append("Username is already taken.")
            return render(request, "signup.html", context)

        user = User.objects.create_user(username, email, password)
        user.last_name = last_name
        user.first_name = first_name
        user.email = email
        user.save()

        group = Group.objects.get(name='rider')
        user.groups.add(group)
        Riders.objects.create(user=user)

        return HttpResponseRedirect('/login')

    return render(request, "signup.html", context)


def rider_home(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        img = request.POST.get('img', '')

        if not user.is_authenticated:
            return HttpResponseRedirect('/login')

        host = "http://b1c9f666.ngrok.io"
        paypal_dict = {
            "business": "false.namebad-facilitator@gmail.com",
            "amount": amount,
            "item_name": "tab",
            "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
            "return": host + "/payment/done/",
            "cancel_return": 'http://{}{}'.format(host, reverse('canceled')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)

        return render(request, "rider/checkout.html", {'amount': amount, 'form': form, 'name': name, 'img': img})

    else:
        user = request.user
        establishments = Establishments.objects.all()

        if not user.is_authenticated:
            return HttpResponseRedirect('/login')
        elif user.groups.filter(name='establishment').exists():
            return HttpResponseRedirect('/establishmentHome')

        return render(request, "rider/rider_home.html", {'establishments': establishments})


def confirm(request):
    context = {
        'data': {},
        'errors': [],
    }

    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')

    return render(request, "rider/confirm.html", context)


def establishment_home(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    elif user.groups.filter(name='rider').exists():
        return HttpResponseRedirect('/riderHome')

    trips = Trips.objects.filter(establishment__user=user)

    return render(request, "establishment/establishment_home.html", {'trips': trips})


def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/login')
