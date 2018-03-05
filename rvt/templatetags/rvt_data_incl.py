from django import template
from rvt.models import RVTvInfo, RVTvDisk, RVTvPartition, RVTvDatastore, RVTvHost
from django.db.models import Sum

#Some init stuff
register = template.Library()


@register.inclusion_tag('rvt/rvt_vpartitions_tbl.html')
def show_vpartitions(batch):
    vPart = RVTvPartition.objects.filter(rvt_vi_batch=batch)

    formula = RVTvPartition.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vp_capacitymb'))
    capacitymb = formula['rvt_vp_capacitymb__sum']
    capacity = capacitymb / 1000 / 1000

    formula = RVTvPartition.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vp_consumedmb'))
    consumedmb = formula['rvt_vp_consumedmb__sum']
    consumed = consumedmb / 1000 / 1000

    formula = RVTvPartition.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vp_freemb'))
    freemb = formula['rvt_vp_freemb__sum']
    free = freemb / 1000 / 1000

    return {
        'vpart': vPart,
        'capacity': capacity,
        'consumed': consumed,
        'free': free,
    }


@register.inclusion_tag('rvt/rvt_vdisks_tbl.html')
def show_vdisks(batch):
    vdisks = RVTvDisk.objects.filter(rvt_vi_batch=batch)

    formula = RVTvDisk.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vd_capacitymb'))
    capacitymb = formula['rvt_vd_capacitymb__sum']
    capacity = capacitymb / 1000 / 1000
    formula = RVTvDisk.objects.filter(rvt_vd_diskmode='independent_persistent')
    rdmcount = formula.count()
    formula = RVTvDisk.objects.filter(rvt_vd_thin=True)
    thincount = formula.count()
    formula = RVTvDisk.objects.filter(rvt_vd_thin=False)
    thickcount = formula.count()

    return {'vdisks': vdisks, 'capacity': capacity, 'rdmcount': rdmcount, 'thincount': thincount, 'thickcount': thickcount}


@register.inclusion_tag('rvt/rvt_vdatastores_tbl.html')
def show_vdatastores(batch):
    vdatastores = RVTvDatastore.objects.filter(rvt_vi_batch=batch)

    formula = RVTvDatastore.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vs_capacitymb'))
    capacitymb = formula['rvt_vs_capacitymb__sum']
    capacity = capacitymb / 1000 / 1000

    formula = RVTvDatastore.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vs_provisionedmb'))
    provmb = formula['rvt_vs_provisionedmb__sum']
    prov = provmb / 1000 / 1000

    formula = RVTvDatastore.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vs_usedmb'))
    usedmb = formula['rvt_vs_usedmb__sum']
    used = usedmb / 1000 / 1000

    formula = RVTvDatastore.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vs_freemb'))
    freemb = formula['rvt_vs_freemb__sum']
    free = freemb / 1000 / 1000


    return {'vdatastores': vdatastores, 'capacity': capacity, 'prov': prov, 'used': used, 'free': free,}



@register.inclusion_tag('rvt/rvt_vinfo_tbl.html')
def show_vinfo(batch):
    vinfo = RVTvInfo.objects.filter(rvt_vi_batch=batch)

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_unshared_mb'))
    unsharedmb = formula['rvt_vi_unshared_mb__sum']
    unshared = unsharedmb / 1000 / 1000

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_in_use_mb'))
    usedmb = formula['rvt_vi_in_use_mb__sum']
    used = usedmb / 1000 / 1000

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_provisioned_mb'))
    provmb = formula['rvt_vi_provisioned_mb__sum']
    prov = provmb / 1000 / 1000

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_disks'))
    disktotal = formula['rvt_vi_disks__sum']

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_cpus'))
    cputotal = formula['rvt_vi_cpus__sum']
    vcputovm = cputotal / vinfo.count()

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_memory'))
    memory = formula['rvt_vi_memory__sum']/1000
    memorytovm = memory / vinfo.count()

    return {
        'vinfo': vinfo,
        'unshared': unshared,
        'used': used,
        'prov': prov,
        'pwron': RVTvInfo.objects.filter(rvt_vi_powerstate="poweredOn").count(),
        'pwroff': RVTvInfo.objects.filter(rvt_vi_powerstate="poweredOff").count(),
        'disktotal': disktotal,
        'cputotal': cputotal,
        'vcputovm': vcputovm,
        'memory': memory,
        'memorytovm': memorytovm,
    }


@register.inclusion_tag('rvt/rvt_vhosts_tbl.html')
def show_vhosts(batch):
    vhosts = RVTvHost.objects.filter(rvt_vi_batch=batch)

    formula = RVTvHost.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vh_socketcount'))
    totalsockets = formula['rvt_vh_socketcount__sum']

    formula = RVTvHost.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vh_socketcores'))
    totalcores = formula['rvt_vh_socketcores__sum']

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_cpus'))
    cputotal = formula['rvt_vi_cpus__sum']
    vcputopcore = cputotal / totalcores

    formula = RVTvHost.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vh_memorymb'))
    memorymb = formula['rvt_vh_memorymb__sum']/1000

    formula = RVTvHost.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vh_vram'))
    vrammb = formula['rvt_vh_vram__sum']/1000

    formula = RVTvHost.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vh_usedmem'))
    vmumb = formula['rvt_vh_usedmem__sum']/1000

    return {
        'vhosts': vhosts,
        'totalsockets': totalsockets,
        'totalcores': totalcores,
        'cputotal': cputotal,
        'vcputopcore': vcputopcore,
        'memorymb': memorymb,
        'vrammb': vrammb,
        'vmumb': vmumb,
    }


@register.inclusion_tag('rvt/rvt_brief_tbl.html')
def show_brief(batch):
    vinfo = RVTvInfo.objects.filter(rvt_vi_batch=batch)
    vdisks = RVTvDisk.objects.filter(rvt_vi_batch=batch)
    vPart = RVTvPartition.objects.filter(rvt_vi_batch=batch)

    formula = RVTvPartition.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vp_consumedmb'))
    consumedmb = formula['rvt_vp_consumedmb__sum']
    consumed = consumedmb / 1000 / 1000

    formula = RVTvDisk.objects.filter(rvt_vd_diskmode='independent_persistent')
    rdmcount = formula.count()

    formula = RVTvInfo.objects.filter(rvt_vi_batch=batch).aggregate(Sum('rvt_vi_in_use_mb'))
    usedmb = formula['rvt_vi_in_use_mb__sum']
    used = usedmb / 1000 / 1000

    return {
        'vdisks': vdisks,
        'rdmcount': rdmcount,
        'vinfo': vinfo,
        'used': used,
        'vpart': vPart,
        'consumed': consumed,
    }
