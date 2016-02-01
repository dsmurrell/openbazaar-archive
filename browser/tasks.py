from __future__ import absolute_import

from celery import shared_task
import json, grequests
from browser.models import Node

from django.db.models.fields.related import ManyToManyField

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

	defaults['facebook'] = profile['']
	defaults['instagram'] = profile['']
	defaults['snapchat'] = profile['']
	defaults['twitter'] = profile['']

	defaults['last_seen'] = profile['']
	return defaults

@shared_task
def scrape_profiles():
	print "def scrape profiles"
	nodes = json.load(open("/Users/daniel/repos/openbazaar/crawler/nodes.json", 'r'))
	#print json.dumps(nodes, sort_keys=True, indent=4)
	print 'Read ', len(nodes), ' nodes from nodes.json'

	def exception_handler(request, exception):
		pass

	def profile_request(guid=''):
		return 'http://localhost:18469/api/v1/profile?guid=' + guid

	active_profiles = []
	urls = [profile_request(k) for k, v in nodes.items()]	
	requests = (grequests.get(url, timeout=5) for url in urls)
	responses = grequests.map(requests, exception_handler=exception_handler)
	for response in responses:
		if response is not None:
			if response.content == '{}':
				pass
			else:
				d = json.loads(response.content)
				#print json.dumps(d, sort_keys=True, indent=4)
				active_profiles.append(d['profile'])

	print len(active_profiles), ' active profiles found.'
	
	for ap in active_profiles:
		#node = Node()
		#node_defaults = to_dict(node)
		defaults = construct_profile_defaults(ap)
		node, created = Node.objects.update_or_create(guid=ap['guid'], defaults=defaults)
		node.save()

	#print json.dumps(node_defaults, sort_keys=True, indent=4)

	#print json.dumps(active_profiles[0], sort_keys=True, indent=4)

	# for ap in active_profiles:
	# 	print 'name ', ap['profile']['name']
	# 	node = Node()
	# 	defailts = to_dict(node)
		
	# 	obj, created = Person.objects.update_or_create(first_name='John', last_name='Lennon', defaults=updated_values)
	# 	try:
	# 	    obj = Node.objects.get(guid=ap['profile']['guid'])
	# 	    for key, value in updated_values.iteritems():
	# 	        setattr(obj, key, value)
	# 	    obj.save()
	# 	except Person.DoesNotExist:
	# 	    updated_values.update({'first_name': 'John', 'last_name': 'Lennon'})
	# 	    obj = Person(**updated_values)
	# 	    obj.save()
	# 	Node = new Node()

@shared_task
def add(x, y):
	print 'adding two numbers!'
	return x + y