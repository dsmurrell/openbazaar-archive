from django.contrib import admin

# Register your models here.
from browser.models import Node, Network, Follower, Blocked, Store, Moderator, Listing, Address

#class BankTransactionAdmin(admin.ModelAdmin):
#    search_fields = ["sender", "reference", "amount_in", "amount_out", "bank_account__account_number"]
#admin.site.register(BankTransaction, BankTransactionAdmin)

class NodeAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']

admin.site.register(Node, NodeAdmin)
admin.site.register(Network)
admin.site.register(Follower)
admin.site.register(Blocked)
admin.site.register(Store)
admin.site.register(Moderator)
admin.site.register(Listing)
admin.site.register(Address)

