from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'point']
    list_filter = ['user', 'post', 'point']

admin.site.register(Account,AccountAdmin)

# Перенос авторов из группы Actions Required
def make_author(modeladmin,request,queryset):
    group = Group.objects.get(name='Authors')
    ungroup = Group.objects.get(name='Actions Required')
    for user in queryset:
        user.groups.add(group)
        user.groups.remove(ungroup)

make_author.short_description = "Утвердить автора"

# Добавление действия в панель администрирования.
class CustomUserAdmin(UserAdmin):
    actions = [make_author]
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
