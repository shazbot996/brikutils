from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import re

def index(request):
    if request.user.is_authenticated:
        message = ""
        return render(request, "app/app_index.html", {'message': message, 'style': "alert-success"})
    else:
        message = "You'll need to log in do anything here"
        return render(request, 'app/app_index.html', {'message': message, 'style': "alert-danger"})


@login_required
def me(request):
    referer = get_referer_view(request)

    if referer == "/login":
        message = "%s %s" % ("Login Successful, ", request.user.get_full_name())
        style = "alert-success"

    else:
        message = "%s %s" % ("Hello  ", request.user.get_full_name())
        style = "alert-info"

    return render(request, 'app/app_me.html', {'message': message, 'style': style})


def initadmin(request):
    User.objects.create_superuser('bkadmin', 'admin@example.com', 'rubrik123')  # @TODO REMOVE
    message = "Admin User 'bkadmin' Initialized!"
    return render(request, "app/app_index.html", {'message': message})


def get_referer_view(request, default=None):

    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')

    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer
