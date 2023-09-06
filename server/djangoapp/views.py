from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from . import models
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealers_by_id, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login , logout , authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', {
                "message": "Logged in!"})
        else:
            return render(request, "djangoapp/index.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "djangoapp/index.html")


def logout_view(request):
    logout(request)
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]

        # Ensure password matches confirmation
 

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
            user.save()
        except IntegrityError:
            return render(request, "djangoapp/registration.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, "djangoapp/index.html")
    else:
        return render(request, "djangoapp/registration.html")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        print(request.GET.keys())
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/2a3dac3c-7f9d-484d-84d4-716d2585a304/dealership-package/get-dealership.json"
        # Get dealers from the URL
        #dealerships = get_dealers_from_cf(url)
        if request.GET.get('state'):
            context['dealerships'] = get_dealers_by_state(url, request.GET['state'])
            #context['state'] = request.GET('state')
        elif request.GET.get('id'):
            context['dealerships'] = get_dealers_by_id(url, request.GET['id'])
        else:
            context['dealerships'] = get_dealers_from_cf(url)
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    url = 'https://us-south.functions.appdomain.cloud/api/v1/web/2a3dac3c-7f9d-484d-84d4-716d2585a304/dealership-package/get-review.json'
    context['reviews'] = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
    
    return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == 'POST':
        if request.user.is_autheticated:
            form = request.POST
            review = {
                "name" : "{request.user.first_name} {request.user.last_name}",
                "dealership": dealer_id,
                "review": form['review'],
                "purchase": form.get("purchasecheck"),
            }
            if form.get("purhcasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = models.CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.carmake.name
                review["car_model"] = car.name
                review["car_year"]= car.year.strftime("%Y")
            json_payload = {"review": review}
            print(json_payload)
            url = 'https://us-south.functions.appdomain.cloud/api/v1/web/2a3dac3c-7f9d-484d-84d4-716d2585a304/dealership-package/post-review'
            post_request(url, json_payload, dealer_id=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

    if request.method == 'GET':
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/2a3dac3c-7f9d-484d-84d4-716d2585a304/dealership-package/get-dealership.json?dealerId={0}".format(dealer_id)
        # Get dealers from the URL
        context = {
            "cars": models.CarModel.objects.all(),
            "dealers": get_dealers_from_cf(url),
            "id":dealer_id,
        }
        return render(request, 'djangoapp/add_review.html', context)