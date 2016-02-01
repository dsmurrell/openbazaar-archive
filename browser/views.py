from django.shortcuts import render

from django.http import HttpResponse

from tasks import scrape_profiles


def index(request):
	scrape_profiles.delay()
	return HttpResponse("Hello, world. You're at the polls index.")
