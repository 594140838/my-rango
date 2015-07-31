from django.contrib import admin
from rango.models import *
# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    prepopulated_field = {'slug':('name')}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
admin.site.register(Category,TypeAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)
