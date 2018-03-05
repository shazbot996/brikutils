from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import DeleteView, UpdateView, ListView
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy

#  form & models
from .forms import OrgAddForm, AssessAddForm
from django.db.models import Avg, Max, Min, Sum
from .models import Org, Assessment
from rvt.models import RVTvInfo

@login_required
def index(request):
    message = "Organization List"
    return redirect('/org/list')
    #  return render(request, "org/org_index.html", {'message': message, 'style': "alert-info"})


@login_required
def org_add(request):
    if request.method == "POST":
        thisuser = Org(org_creator=request.user)
        form = OrgAddForm(instance=thisuser, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/org/list')
    else:
        message = ""
        form = OrgAddForm()
        return render(request, "org/org_add_form.html", {'form': form, 'message': message})


@login_required
def org_view(request, record):
    #  prepare our matching org object
    thisorg = Org.objects.get(pk=record)
    #  prepare our matching assessments list
    orgassessments = Assessment.objects.filter(assess_org=record)

    return render(request, "org/org_view.html", {'thisorg': thisorg, 'assessment_list': orgassessments})


class MyOrgList(ListView):
    model = Org

    def get_queryset(self):
        return Org.objects.filter(org_creator=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrgUpdate(UpdateView):
    model = Org
    fields = ['org_name', 'org_email',]
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        messages.success(self.request, "Record Saved!")
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrgDelete(DeleteView):
    model=Org
    success_url = reverse_lazy('org_list')


@login_required
def assess_add(request):
    if request.method == "POST":
        thisuser = Assessment(assess_creator=request.user)
        form = AssessAddForm(request.user, instance=thisuser, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/org/assessment')
    else:
        message = ""
        form = AssessAddForm(request.user)
        return render(request, "org/assessment_add_form.html", {'form': form, 'message': message})


@login_required
def assess_view(request, record):
    #  prepare our matching org object
    thisassessment = Assessment.objects.get(pk=record)
    batches = RVTvInfo.objects.values_list('rvt_vi_batch', flat=True).distinct()
    return render(request, "org/assessment_view.html", {'thisassessment': thisassessment, 'batches': batches})


class MyAssessList(ListView):
    model = Assessment

    def get_queryset(self):
        return Assessment.objects.filter(assess_creator=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AssessUpdate(UpdateView):
    model = Assessment
    fields = ['assess_name',]
    template_name_suffix = '_update_form'


    def form_valid(self, form):
        messages.success(self.request, "Record Saved!")
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AssessDelete(DeleteView):
    model=Assessment
    success_url = reverse_lazy('assess_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


