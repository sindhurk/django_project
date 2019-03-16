from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

import json, requests
from datetime import datetime, timedelta


def home(request):

	url = "https://www.reddit.com/top.json?limit=45"

	r= requests.get(url, headers = {'User-agent': 'your bot 0.1'}).json()

	topstories = []
	
	for child in r['data']['children']:
		dictionary = {}
		dictionary['title']=child['data']['title']
		author=child['data']['author']
		link_to_author = "https://www.reddit.com/user/"+author
		dictionary['author']=author
		dictionary['link_to_author']=link_to_author
		unix_ts=child['data']['created_utc']
		dictionary['timestamp']=(datetime.fromtimestamp(unix_ts) + timedelta(hours=5.30)).strftime('%d-%b-%Y %I:%M %p')
		try:
			gif = 'gif'
			image = child['data']['preview']['images'][0]['source']['url']
			if gif not in image:
				dictionary['link_to_image']=child['data']['preview']['images'][0]['source']['url']
		except:
			continue

		topstories.append(dictionary)
		pagination = Paginator(topstories, 15)


	return render(request, 'home.html', {'topjson': pagination.page(request.GET.get('page', 1))})