import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'archive.settings'
import django
django.setup()
from browser.models import Node
from browser.tasks import scrape_profiles, get_avatars

scrape_profiles()
get_avatars()

# nodes = Node.objects.all()
# for node in nodes:
#     print node.name
#     print node.avatar
#     if node.avatar:
#         print node.avatar.url