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
		if searchCategory == 'cuisines':
			cuisine_id = ''
			cusineResponse = p.getCuisines(city_id = '4')
			for num, cuisine in enumerate(cusineResponse['cuisines']):
				if cuisine['cuisine']['cuisine_name'] == searchKeyWord:
					cuisine_id = cuisine['cuisine']['cuisine_id']
			response = p.search(entity_type="city", entity_id='4',cuisines=cuisine_id)
		if searchCategory == 'restaurantType':
			restaurantTypeValue = ''
			restaurantTypeResponse = p.getEstablishments(city_id = '4')
			for num, establishment in enumerate(restaurantTypeResponse['establishments']):
				if establishment['establishment']['name'] == searchKeyWord:
					restaurantTypeValue = establishment['establishment']['id']
			response = p.search(entity_type="city", entity_id='4', establishment_type=restaurantTypeValue)
		if searchCategory == 'restaurantCategory':
			category_id = ''
			category_response = p.getCategories()
			for num, category in enumerate(category_response['categories']):
				if category['categories']['name'] == searchKeyWord:
					category_id = category['categories']['id']
			response = p.search(entity_type="city", entity_id='4', category=category_id)
	except Exception as e:
		print(e)
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
		print('failed in for loop')
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
	featured_image=restDetails['featured_image']
	details = [dict() for x in range(12)]
	details = {'id':id, 'name':name, 'name':name, 'address':address, 'average_cost_for_two':average_cost_for_two,'featured_image':featured_image, 
	'thumbnail':thumbnail, 'rating':rating, 'popular_opinion':popular_opinion, 'photos':photos, 'menu':menu,'cuisines': cuisines,'votes':votes}
	request.session[0]=value
	request.session[1]=details
	all_enties = RestaurantReview.objects.all().filter(restaurantId=value)
	reviewList = []
	for p in all_enties:
		reviewElement = [dict() for x in range(9)]
		review = p.review
		rating = p.rating
		userName = p.user
		reviewElement={'review':review,'rating':rating, 'userName':userName}
		reviewList.append(reviewElement)
	return render(request, 'restaurantview.html', {'restdetails':details, 'reviewsAndRatings':reviewList})
	
@login_required
def submit(request):
	print('Submit click is working')
	error = ''
	details=request.session['1']
	reviewList=''
	review = request.GET.get('review')
	rating = '4'
	user = request.user
	id= request.session['0']
	if not review:
		error = 'Please write a review'
	elif not rating:
		error = 'Please give a rating'
	else:	
		obj, created = RestaurantReview.objects.update_or_create(user=user,restaurantId=id, defaults = {'review':review,'rating':rating})
	all_enties = RestaurantReview.objects.all().filter(restaurantId=id)
	reviewList = []
	for p in all_enties:
		reviewElement = [dict() for x in range(9)]
		review = p.review
		rating = p.rating
		userName = p.user
		reviewElement={'review':review,'rating':rating, 'userName':userName}
		reviewList.append(reviewElement)
	return render(request, 'restaurantview.html', {'error':error, 'restdetails':details,'reviewsAndRatings':reviewList})