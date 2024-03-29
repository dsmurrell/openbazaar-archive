# source: http://cramer.io/2008/08/08/custom-fields-in-django/

# from django.db import models

# class SeparatedValuesField(models.TextField):
#     __metaclass__ = models.SubfieldBase

#     def __init__(self, *args, **kwargs):
#         self.token = kwargs.pop('token', ',')
#         super(SeparatedValuesField, self).__init__(*args, **kwargs)

#     def to_python(self, value):
#         if not value: return
#         if isinstance(value, list):
#             return value
#         return value.split(self.token)

#     def get_db_prep_value(self, value):
#         if not value: return
#         assert(isinstance(value, list) or isinstance(value, tuple))
#         return self.token.join([unicode(s) for s in value])

#     def value_to_string(self, obj):
#         value = self._get_val_from_obj(obj)
#         return self.get_db_prep_value(value)

# try:
#     import cPickle as pickle
# except:
#     import pickle
# import base64

# class SerializedDataField(models.TextField):
#     """Because Django for some reason feels its needed to repeatedly call
#     to_python even after it's been converted this does not support strings."""
#     __metaclass__ = models.SubfieldBase

#     def to_python(self, value):
#         if value is None: return
#         if not isinstance(value, basestring): return value
#         value = pickle.loads(base64.b64decode(value))
#         return value

#     def get_db_prep_save(self, value):
#         if value is None: return
#         return base64.b64encode(pickle.dumps(value))