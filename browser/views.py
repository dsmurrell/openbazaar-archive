from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render_to_response, render

from tasks import scrape_profiles, get_avatars

from models import Node

def vendors(request):
	nodes = Node.objects.all()
	context = {'nodes': nodes}
	return render(request, 'vendors.html', context)
