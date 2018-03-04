from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from .forms import VMdataForm
from .models import VMdata
from autobrik.models import Game

@login_required
def index(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()

    return render(request, "autobrik/home.html",
                  {'games': active_games})

def upload_csv(request):
    return render(request, "autobrik/home.html")  # fix this

@login_required
def new_vmdata(request):
    if request.method == "POST":
        thisuser = VMdata(rvt_user=request.user)
        form = VMdataForm(instance=thisuser, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('autobrik_home')
    else:
        form = VMdataForm()
    return render(request, "autobrik/new_vmdata_form.html", {'form': form})

class AllVMdataList(ListView):
    model = VMdata
