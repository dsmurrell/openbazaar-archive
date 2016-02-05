from __future__ import absolute_import

from celery import shared_task
import json, grequests, datetime
from browser.models import Node
from django.utils import timezone

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.db.models.fields.related import ManyToManyField

# converts object instance to dictionary
def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data

# exception handler for grequests.map
def exception_handler(request, exception):
		pass

@shared_task
def scrape_profiles():
	nodes = json.load(open("/Users/daniel/repos/openbazaar/crawler/nodes.json", 'r'))
	#print json.dumps(nodes, sort_keys=True, indent=4)
	#node = Node()
	#node_defaults = to_dict(node)
	print 'Read ' + str(len(nodes)) + ' nodes from nodes.json'

	def exception_handler(request, exception):
		pass

	def profile_request(guid=''):
		return 'http://localhost:18469/api/v1/profile?guid=' + guid

	active_profiles = []
	urls = [profile_request(k) for k, v in nodes.items()]	
	requests = (grequests.get(url, timeout=10) for url in urls)
	responses = grequests.map(requests, exception_handler=exception_handler)
	for response in responses:
		if response is not None:
			if response.content == '{}':
				pass
			else:
				d = json.loads(response.content)
				#print json.dumps(d, sort_keys=True, indent=4)
				active_profiles.append(d['profile'])

	print str(len(active_profiles)) + ' active profiles found.'
	
	def construct_profile_defaults(profile):
		defaults = {}
		defaults['about'] = profile['about']
		defaults['avatar_hash'] = profile['avatar_hash']
		defaults['background_color'] = profile['background_color']
		defaults['email'] = profile['email']
		defaults['encryption_key'] = profile['encryption_key']
		defaults['guid'] = profile['guid']
		defaults['handle'] = profile['handle']
		defaults['header_hash'] = profile['header_hash']
		defaults['is_moderator'] = profile['moderator']
		defaults['name'] = profile['name']
		defaults['nsfw'] = profile['nsfw']
		defaults['pgp_key'] = profile['pgp_key']
		defaults['primary_color'] = profile['primary_color']
		defaults['secondary_color'] = profile['secondary_color']
		defaults['short_description'] = profile['short_description']
		defaults['text_color'] = profile['text_color']
		defaults['is_vendor'] = profile['vendor']
		defaults['website'] = profile['website']

		defaults['facebook'] = ''
		defaults['instagram'] = ''
		defaults['snapchat'] = ''
		defaults['twitter'] = ''

		defaults['last_seen'] = timezone.now()
		return defaults

	# save new active profiles to the database and update old ones
	new_profiles = 0
	for ap in active_profiles:
		defaults = construct_profile_defaults(ap)
		node, created = Node.objects.update_or_create(guid=ap['guid'], defaults=defaults)
		if created:
			new_profiles += 1
		node.save()
	print 'Of which ' + str(new_profiles) + ' are new profiles.'

@shared_task
def get_avatars():
	def get_image_request(guid='', hash=''):
		return 'http://localhost:18469/api/v1/get_image?guid=' + guid + '&hash=' + hash

	urls = []
	for node in Node.objects.all():
		if node.avatar_hash:
 			urls.append(get_image_request(node.guid, node.avatar_hash))

 	available_avatars = []
 	requests = (grequests.get(url, timeout=10) for url in urls)
	responses = grequests.map(requests, exception_handler=exception_handler)
	for response in responses:
		if response is not None:
			avatar_hash = response.url.split('hash=')[1]
			node = Node.objects.get(avatar_hash=avatar_hash)
			if node is not None:
				print avatar_hash
				avatar_temp = NamedTemporaryFile(delete=True)
				avatar_temp.write(response.content)
				avatar_temp.flush()
				node.avatar.save(avatar_hash, File(avatar_temp))
			#avatar = response.content
			#print json.dumps(d, sort_keys=True, indent=4)
			#active_profiles.append(d['profile'])
		

	#newdoc = Document(docfile = request.FILES['docfile'])
    #newdoc.save()



@shared_task
def add(x, y):
	print 'adding two numbers!'
	return x + y