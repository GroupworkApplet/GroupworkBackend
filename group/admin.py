from django.contrib import admin
from .models import *

admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Message)
admin.site.register(Document)
admin.site.register(Progress)
# Register your models here.
