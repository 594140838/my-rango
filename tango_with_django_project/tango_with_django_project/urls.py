#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static', #指定视图函数所在模块的位置，可以为空，那样的话后面视图函数路径就要详细指出
        (r'^media/(?P<path>.*)', #指定当访问 /media/xx 时，调用后面的函数
        'serve', #引用django.views.static模块下的serve函数，该函数会将匹配到的文件传送到客户端浏览器
        {'document_root': settings.MEDIA_ROOT}), )#指定匹配到的媒体文件所放置的目录 
