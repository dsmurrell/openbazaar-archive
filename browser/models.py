from __future__ import unicode_literals

from django.db import models
#from custom_fields import *

class Node(models.Model):
	guid = models.CharField(max_length=40)
	last_seen = models.DateTimeField()
	#first_seen = models.DateTimeField()

	name = models.CharField(max_length=100)
	handle = models.CharField(max_length=100)
	short_description = models.CharField(max_length=200)
	nsfw = models.BooleanField(default=0)
	avatar_hash = models.CharField(max_length=40)
	avatar = models.ImageField(upload_to='avatars', null=True)
	
	website = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	facebook = models.CharField(max_length=100)
	twitter = models.CharField(max_length=100)
	instagram = models.CharField(max_length=100)
	snapchat = models.CharField(max_length=100)
	pgp_key = models.CharField(max_length=100)

	about = models.CharField(max_length=1000)

	encryption_key = models.CharField(max_length=100)
	header_hash = models.CharField(max_length=40)
	text_color = models.CharField(max_length=100)
	primary_color = models.CharField(max_length=100)
	secondary_color = models.CharField(max_length=100)
	background_color = models.CharField(max_length=100)

	is_vendor = models.BooleanField(default=0)
	is_moderator = models.BooleanField(default=0)

	# override avatar image file on save
	def save(self, *args, **kwargs):
	    try:
	        this = Node.objects.get(id=self.id)
	        if this.avatar != self.avatar:
	            this.avatar.delete()
	    except: pass
	    super(Node, self).save(*args, **kwargs)

class Network(models.Model):
	ip_address = models.GenericIPAddressField()
	port = models.IntegerField()

class Follower(models.Model):
	followed_node = models.ForeignKey('Node', related_name='followed_node', on_delete=models.CASCADE)
	following_node = models.ForeignKey('Node', related_name='following_node', on_delete=models.CASCADE)

class Blocked(models.Model):
	blocked_node = models.ForeignKey('Node', related_name='blocked_node', on_delete=models.CASCADE)
	blocking_node = models.ForeignKey('Node', related_name='blocking_node', on_delete=models.CASCADE)

class Store(models.Model):
	node = models.ForeignKey(Node, on_delete=models.CASCADE)
	visible = models.BooleanField(default=0)
	tags = models.CharField(max_length=100)
	terms = models.CharField(max_length=1000)
	return_policy = models.CharField(max_length=1000)

class Moderator(models.Model):
	node = models.ForeignKey(Node, on_delete=models.CASCADE)
	moderation_fee = models.DecimalField(max_digits=8, decimal_places=8)

class Listing(models.Model):
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	contract_hash = models.CharField(max_length=40)
	last_seen = models.DateTimeField()
	#first_seen = models.DateTimeField()

	title = models.CharField(max_length=100)
	category = models.CharField(max_length=40)
	nsfw = models.BooleanField(default=0)
	thumbnail_hash = models.CharField(max_length=40)
	price = models.DecimalField(max_digits=8, decimal_places=8)
	origin = models.CharField(max_length=100)
	currency_code = models.CharField(max_length=5)

class Address(models.Model):
	node = models.ForeignKey(Node, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
