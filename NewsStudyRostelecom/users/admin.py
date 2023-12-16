from django.contrib import admin

from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'point']
    list_filter = ['user', 'post', 'point']

admin.site.register(Account,AccountAdmin)