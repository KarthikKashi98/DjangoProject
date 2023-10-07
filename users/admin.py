from django.contrib import admin
from .models import Main_User_Info
from .models import UserInfo,GroupsMembers,GroupInfo
admin.site.register(Main_User_Info)
admin.site.register(UserInfo)
admin.site.register(GroupsMembers)
admin.site.register(GroupInfo)



# Register your models here.
