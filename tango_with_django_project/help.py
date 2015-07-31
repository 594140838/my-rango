#coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')
import django
django.setup()

from rango.models import Category,Page

def add_page(category,title,url):
    page = Page.objects.get_or_create(category=category,title=title,url=url)[0] #返回a tuple (object,created)
    return page
def add_category(name,views=0,likes=0):
    category  = Category.objects.get_or_create(name=name,views=views,likes=likes,slug=name)[0]
    return category

def operating():
    python_type = add_category('Python')

    add_page(category=python_type,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/")

    add_page(category=python_type,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_page(category=python_type,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    django_type = add_category("Django")

    add_page(category=django_type,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(category=django_type,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(category=django_type,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    frame_type = add_category("Other Frameworks")

    add_page(category=frame_type,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(category=frame_type,
        title="Flask",
        url="http://flask.pocoo.org")

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

if __name__ == '__main__':
    print ("开始执行Rango自动化脚本...")
    operating()
