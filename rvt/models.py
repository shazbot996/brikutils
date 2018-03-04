from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User



class RVTvInfoQuerySet(models.QuerySet):
    def records_for_user(self, user):
        return self.filter(rvt_vi_user=user)

    def batches(self, user):
        return self.filter(rvt_vi_user=user).distinct('rvt_vi_batch')

    def records_for_batch(self, user, batch):
        return self.filter(rvt_vi_user=user, rvt_vi_batch=batch)


class RVTvInfo(models.Model):
    rvt_vi_user = models.ForeignKey(User, related_name="rvt_vi_user", default='1', on_delete=models.CASCADE)
    rvt_vi_assessment = models.ForeignKey('org.Assessment', related_name="rvt_vi_assessment", default='1', on_delete=models.CASCADE)
    rvt_vi_batch = models.IntegerField(null=True)
    rvt_vi_filename = models.CharField(max_length=300, blank=False)
    rvt_vi_vm = models.CharField(max_length=300, blank=True)
    rvt_vi_powerstate = models.CharField(max_length=300)
    rvt_vi_guest_state = models.CharField(max_length=300)
    rvt_vi_provisioned_mb = models.IntegerField(null=True)
    rvt_vi_in_use_mb = models.IntegerField(null=True)
    rvt_vi_unshared_mb = models.IntegerField(null=True)
    load_vi_time = models.DateTimeField(auto_now_add=True)
    last_vi_edit = models.DateTimeField(auto_now=True)

    objects = RVTvInfoQuerySet.as_manager()
