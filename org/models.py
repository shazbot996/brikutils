from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse


class OrgInfoQuerySet(models.QuerySet):
    def records_for_user(self, user):
        return self.filter(org_creator=user)


class Org(models.Model):
    org_creator = models.ForeignKey(User, related_name='org_creator', on_delete=models.CASCADE)
    org_name = models.CharField(max_length=300, blank=False, verbose_name='Name')
    org_contact = models.CharField(max_length=300, blank=False, verbose_name='Contact')
    org_email = models.EmailField(blank=False, verbose_name='Email')
    load_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    objects = OrgInfoQuerySet.as_manager()

    def __str__(self):
        return u'{0}'.format(self.org_name)

    def get_absolute_url(self):
        return reverse('org-update', kwargs={'pk': self.pk})

    #  def delete(self, *args, **kwargs):
    #    if Assessment.objects.filter(assess_org_id=self.pk).exists():
    #        raise Exception('This record still has assessments that would be orphaned. Aborting.')
    #
    #    super().delete(*args, **kwargs)


class AssessInfoQuerySet(models.QuerySet):
    def records_for_user(self, user):
        return self.filter(org_creator=user)

    def records_for_org(self, org):
        return self.filter(assess_org=org)


class Assessment(models.Model):
    assess_creator = models.ForeignKey(User, related_name="assess_creator", on_delete=models.CASCADE)
    assess_org = models.ForeignKey(Org, related_name="assess_org", on_delete=models.CASCADE)
    assess_name = models.CharField(max_length=300, blank=False, verbose_name="assess_name")
    load_time = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    objects = AssessInfoQuerySet.as_manager()

    def __str__(self):
        return u'{0}'.format(self.assess_name)

    def get_absolute_url(self):
        return reverse('assess_update', kwargs={'pk': self.pk})
