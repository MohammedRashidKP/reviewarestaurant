from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import requests
import os
import sys
from django.http import HttpResponse
from pyzomato import Pyzomato
import json
from .models import RestaurantReview


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        print(request)
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
	
@login_required
def search(request):
	p = Pyzomato('ca5cbda00917434b4886bcf7fcc01b97')
	list = []
	try:
		searchCategory = request.GET.get('searchCategory','')
		searchKeyWord = request.GET.get('searchKeyWord','')
		response=''
		print(searchKeyWord)
		if searchCategory == 'cuisines':
			response = p.search(q="bangalore", cuisines=searchKeyWord)
		if searchCategory == 'restaurantType':
			response = p.search(q="bangalore", establishment_type=searchKeyWord)
		if searchCategory == 'restaurantCategory':
			response = p.search(q="bangalore", category=searchKeyWord)
	except:
		print("Error")
	try:
		for num, restaurant in enumerate(response['restaurants']):
			number= num+1,
			name=restaurant['restaurant']['name']
			name = name.format()
			url=restaurant['restaurant']['url']
			cuisines=restaurant['restaurant']['cuisines']
			rating=restaurant['restaurant']['user_rating']['aggregate_rating']
			icon=restaurant['restaurant']['thumb']
			price=restaurant['restaurant']['average_cost_for_two']
			res_id=restaurant['restaurant']['id']
			dictlist = [dict() for x in range(9)]
			dictlist={'number':number, 'name':name, 'url':url, 'cuisines':cuisines, 'rating':rating, 'icon':icon, 'price':price, 'res_id':res_id }
			list.append(dictlist)
	except Exception as e:
		print(e)
	return render(request, 'home.html', {'context': list})
	
@login_required
def showRestaurantDetails(request, value):
	p = Pyzomato('ca5cbda00917434b4886bcf7fcc01b97')
	restDetails = p.getRestaurantDetails(value)
	id = value
	name=restDetails["name"]
	url=restDetails["url"]
	address=restDetails['location']['address']
	cuisines=restDetails['cuisines']
	average_cost_for_two=restDetails['average_cost_for_two']
	thumbnail=restDetails['thumb']
	rating=restDetails['user_rating']['aggregate_rating']
	popular_opinion=restDetails['user_rating']['rating_text']
	votes=restDetails['user_rating']['votes']
	photos=restDetails['photos_url']
	menu=restDetails['menu_url']
	details = [dict() for x in range(12)]
	request.session[0]=value
	details={'id':id,'name':name, 'url':url, 'address':address, 'cuisines':cuisines, 'cuisines':cuisines, 'average_cost_for_two':average_cost_for_two, 'thumbnail':thumbnail, 'rating':rating, 'popular_opinion':popular_opinion,'votes':votes,'photos':photos,'menu':menu}
	return render(request, 'restaurantview.html', {'restdetails':details})
	
@login_required
def submit(request):
	review = request.GET.get('review')
	rating = request.GET.get('rating')
	user = request.user
	id= request.session['0']
	r = RestaurantReview(user=user, restaurantId=id, review=review,rating=rating)
	r.save()
	all_enties = RestaurantReview.objects.all()
	reviewList = []
	for p in all_enties:
		reviewList.append(p.review)
	print(reviewList)	
	return render(request, 'restaurantview.html', {'reviewsAndRatings':reviewList})