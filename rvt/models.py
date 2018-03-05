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
    rvt_vi_filename = models.CharField(max_length=300, blank=False, default="UNSET")
    rvt_vi_filename_orig = models.CharField(max_length=300, blank=False, default="UNSET")

    rvt_vi_vm = models.CharField(max_length=300, blank=True, null=True)
    rvt_vi_powerstate = models.CharField(max_length=300, default="UNSET")
    rvt_vi_dnsname = models.CharField(max_length=300, blank=True, null=True)
    rvt_vi_cpus = models.IntegerField(null=True)
    rvt_vi_memory = models.IntegerField(null=True)
    rvt_vi_nics = models.IntegerField(null=True)
    rvt_vi_disks = models.IntegerField(null=True)
    rvt_vi_rsrcpool = models.CharField(max_length=300, default="UNSET")
    rvt_vi_folder = models.CharField(max_length=300, default="UNSET")
    rvt_vi_provisioned_mb = models.IntegerField(null=True)
    rvt_vi_in_use_mb = models.IntegerField(null=True)
    rvt_vi_unshared_mb = models.IntegerField(null=True)
    rvt_vi_hwversion = models.IntegerField(null=True)
    rvt_vi_path = models.CharField(max_length=300, default="UNSET")
    rvt_vi_datacenter = models.CharField(max_length=300, default="UNSET")
    rvt_vi_cluster = models.CharField(max_length=300, default="UNSET")
    rvt_vi_host = models.CharField(max_length=300, default="UNSET")
    rvt_vi_os_config = models.CharField(max_length=300, default="UNSET")
    rvt_vi_os_vmtools = models.CharField(max_length=300, default="UNSET")
    rvt_vi_id = models.CharField(max_length=300, blank=True, null=True, default="UNSET")
    rvt_vi_uuid = models.CharField(max_length=300, blank=True, null=True, default="UNSET")
    rvt_vi_sdkserver = models.CharField(max_length=300, blank=True, null=True, default="UNSET")
    rvt_vi_sdks_type = models.CharField(max_length=300, blank=True, null=True, default="UNSET")

    load_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    objects = RVTvInfoQuerySet.as_manager()


class RVTvDiskQuerySet(models.QuerySet):
    def records_for_user(self, user):
        return self.filter(rvt_vd_user=user)

    def batches(self, user):
        return self.filter(rvt_vd_user=user).distinct('rvt_vi_batch')

    def records_for_batch(self, user, batch):
        return self.filter(rvt_vd_user=user, rvt_vi_batch=batch)


class RVTvDisk(models.Model):
    rvt_vd_user = models.ForeignKey(User, related_name="rvt_vd_user", default='1', on_delete=models.CASCADE)
    rvt_vi_batch = models.IntegerField(null=True)
    rvt_vd_vmid = models.CharField(max_length=300, blank=True, null=True)
    rvt_vd_disk = models.CharField(max_length=300, default="UNSET")
    rvt_vd_capacitymb = models.IntegerField(null=True)
    rvt_vd_diskmode = models.CharField(max_length=300, blank=True, null=True)
    rvt_vd_thin = models.BooleanField(default=False)
    rvt_vd_controller = models.CharField(max_length=300, default="UNSET")
    rvt_vd_path = models.CharField(max_length=300, default="UNSET")
    rvt_vd_annotation = models.CharField(max_length=300, default="UNSET")

    load_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    objects = RVTvDiskQuerySet.as_manager()


class RVTvPartitionQuerySet(models.QuerySet):
    def records_for_user(self, user):
        return self.filter(rvt_vp_user=user)

    def batches(self, user):
        return self.filter(rvt_vp_user=user).distinct('rvt_vi_batch')

    def records_for_batch(self, user, batch):
        return self.filter(rvt_vp_user=user, rvt_vi_batch=batch)


class RVTvPartition(models.Model):
    rvt_vp_user = models.ForeignKey(User, related_name="rvt_vp_user", default='1', on_delete=models.CASCADE)
    rvt_vi_batch = models.IntegerField(null=True)
    rvt_vp_vmid = models.CharField(max_length=300, blank=True, null=True)
    rvt_vp_disk = models.CharField(max_length=300, default="UNSET")
    rvt_vp_capacitymb = models.IntegerField(null=True)
    rvt_vp_consumedmb = models.IntegerField(null=True)
    rvt_vp_freemb = models.IntegerField(null=True)
    rvt_vp_annotation = models.CharField(max_length=300, default="UNSET")

    load_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    objects = RVTvPartitionQuerySet.as_manager()


class RVTvDatastoreQuerySet(models.QuerySet):
    def records_for_user(self, user):
        return self.filter(rvt_vs_user=user)

    def batches(self, user):
        return self.filter(rvt_vs_user=user).distinct('rvt_vi_batch')

    def records_for_batch(self, user, batch):
        return self.filter(rvt_vs_user=user, rvt_vi_batch=batch)


class RVTvDatastore(models.Model):
    rvt_vs_user = models.ForeignKey(User, related_name="rvt_vs_user", default='1', on_delete=models.CASCADE)
    rvt_vi_batch = models.IntegerField(null=True)
    rvt_vs_name = models.CharField(max_length=300, blank=True, null=True)
    rvt_vs_type = models.CharField(max_length=300, default="UNSET")
    rvt_vs_vmcount = models.IntegerField(null=True)
    rvt_vs_capacitymb = models.IntegerField(null=True)
    rvt_vs_provisionedmb = models.IntegerField(null=True)
    rvt_vs_usedmb = models.IntegerField(null=True)
    rvt_vs_freemb = models.IntegerField(null=True)

    load_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    objects = RVTvDatastoreQuerySet.as_manager()


class RVTvHostQuerySet(models.QuerySet):
    def records_for_user(self, user):
        return self.filter(rvt_vh_user=user)

    def batches(self, user):
        return self.filter(rvt_vh_user=user).distinct('rvt_vi_batch')

    def records_for_batch(self, user, batch):
        return self.filter(rvt_vh_user=user, rvt_vi_batch=batch)


class RVTvHost(models.Model):
    rvt_vh_user = models.ForeignKey(User, related_name="rvt_vh_user", default='1', on_delete=models.CASCADE)
    rvt_vi_batch = models.IntegerField(null=True)

    rvt_vh_hostname = models.CharField(max_length=300, blank=True, null=True)
    rvt_vh_datacenter = models.CharField(max_length=300, blank=True, null=True)
    rvt_vh_cluster = models.CharField(max_length=300, blank=True, null=True)
    rvt_vh_cputype = models.CharField(max_length=300, blank=True, null=True)
    rvt_vh_speed = models.IntegerField(null=True)
    rvt_vh_socketcount = models.IntegerField(null=True)
    rvt_vh_socketcores = models.IntegerField(null=True)
    rvt_vh_cores = models.IntegerField(null=True)
    rvt_vh_cpu_usagepercent = models.IntegerField(null=True)
    rvt_vh_memorymb = models.IntegerField(null=True)
    rvt_vh_mem_usagepercent = models.IntegerField(null=True)
    rvt_vh_vmcount = models.IntegerField(null=True)
    rvt_vh_vmpercore = models.IntegerField(null=True)
    rvt_vh_vcpucount = models.IntegerField(null=True)
    rvt_vh_vcpupercore = models.IntegerField(null=True)
    rvt_vh_vram = models.IntegerField(null=True)
    rvt_vh_usedmem = models.IntegerField(null=True)
    rvt_vh_swapmem = models.IntegerField(null=True)
    rvt_vh_balloonmem = models.IntegerField(null=True)
    rvt_vh_evc = models.CharField(max_length=100, blank=True, null=True)
    rvt_vh_maxevc = models.CharField(max_length=100, blank=True, null=True)
    rvt_vh_esxversion = models.CharField(max_length=300, blank=True, null=True)
    rvt_vh_boottime = models.CharField(max_length=300, blank=True, null=True)

    load_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    objects = RVTvHostQuerySet.as_manager()
