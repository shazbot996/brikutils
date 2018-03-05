from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template

from django.views.generic import DeleteView, UpdateView, ListView
from django.urls import reverse_lazy

#  form & models
from .forms import UploadFileForm, OrgForm
from .models import RVTvInfo, RVTvDisk, RVTvPartition, RVTvDatastore, RVTvHost
from django.db.models import Avg, Max, Min, Sum
from org.models import Org, Assessment

#  file includes
import csv, xlrd, os, uuid
from io import TextIOWrapper



@login_required
def index(request):
    message = "Welcome Registered User (RVTOOLS)"
    return render(request, "rvt/rvt_index.html", {'message': message})


@login_required
def upload(request):

    #  not a file - show the form
    if request.method == 'GET':
        form = UploadFileForm()
        assessments = Assessment.objects.filter(assess_creator=request.user)
        return render(request, "rvt/rvt_rvtdataform.html", {'form': form, 'assessments': assessments})

    # is a file - process & display
    else:
        file = request.FILES['file']
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if not file.name.endswith('.xlsx'):
                messages.error(request, 'File is not XLSX type')
                return redirect('rvt_view')

            #  Where are we keeping our files?  @TODO update to model-based
            path = 'uploads/' + request.user.username + '/'
            file_uuid = handle_uploaded_file(file, path)

            #  init the file read - XLS focused here
            wb = xlrd.open_workbook(path + file_uuid)
            sh = wb.sheet_by_name('vInfo')

            #  We're tracking each unique table as a "batch".
            #  let's look up our highest batch number & increment to the next when we save the record
            try:
                maxbatch = RVTvInfo.objects.order_by('-rvt_vi_batch',)[0]
                nextbatch = maxbatch.rvt_vi_batch + 1
            except:
                nextbatch = 1

            # look up provided ORG id:
            linked_assessment = Assessment.objects.get(id=request.POST['assessment'])

            count = 0

            for row in range(sh.nrows):
                if count == 0:
                    #  grab the header row for top 100 columns
                    hr = [None] * 100
                    for x in range(0, 100):
                        try:
                            hr[x] = sh.cell(row, x).value
                        except:
                            pass

                else:
                    saverecord = RVTvInfo(
                        rvt_vi_user=request.user,
                        rvt_vi_assessment=linked_assessment,
                        rvt_vi_batch=nextbatch,
                        rvt_vi_filename=path + file_uuid,
                        rvt_vi_vm=sh.cell(row, header_col_num(hr, "VM")).value,
                        rvt_vi_powerstate=sh.cell(row, header_col_num(hr, "Powerstate")).value,
                        rvt_vi_dnsname=sh.cell(row, header_col_num(hr, "DNS Name")).value,
                        rvt_vi_cpus=sh.cell(row, header_col_num(hr, "CPUs")).value,
                        rvt_vi_memory=sh.cell(row, header_col_num(hr, "Memory")).value,
                        rvt_vi_nics=sh.cell(row, header_col_num(hr, "NICs")).value,
                        rvt_vi_disks=sh.cell(row, header_col_num(hr, "Disks")).value,
                        rvt_vi_rsrcpool=sh.cell(row, header_col_num(hr, "Resource pool")).value,
                        rvt_vi_folder=sh.cell(row, header_col_num(hr, "Folder")).value,
                        rvt_vi_provisioned_mb=sh.cell(row, header_col_num(hr, "Provisioned MB")).value,
                        rvt_vi_in_use_mb=sh.cell(row, header_col_num(hr, "In Use MB")).value,
                        rvt_vi_unshared_mb=sh.cell(row, header_col_num(hr, "Unshared MB")).value,
                        rvt_vi_hwversion = sh.cell(row, header_col_num(hr, "HW version")).value,
                        rvt_vi_path=sh.cell(row, header_col_num(hr, "Path")).value,
                        rvt_vi_datacenter=sh.cell(row, header_col_num(hr, "Datacenter")).value,
                        rvt_vi_cluster=sh.cell(row, header_col_num(hr, "Cluster")).value,
                        rvt_vi_host=sh.cell(row, header_col_num(hr, "Host")).value,
                        rvt_vi_os_config=sh.cell(row, header_col_num(hr, "OS according to the configuration file")).value,
                        rvt_vi_os_vmtools=sh.cell(row, header_col_num(hr, "OS according to the VMware Tools")).value,
                        rvt_vi_id=sh.cell(row, header_col_num(hr, "VM ID")).value,
                        rvt_vi_uuid=sh.cell(row, header_col_num(hr, "VM UUID")).value,
                    )
                    vinfo_table = saverecord.save()
                count = count + 1


            #Run through our other worksheets, tie them to this object
            # Call Out to build subroutine
            build_rvt_tables(request, wb, nextbatch)

            #  Cleanup, Aisle Five.
            wb.release_resources()

            topmessage = "%s.%s" % (sh.nrows, ' Records Added!')
            messages.error(request, topmessage)

            return redirect('rvt_view')

        else:
            message = "Form Validation Error! : FileName: "
            return render(request, "rvt/rvt_rvtdataform.html",
                          {'form': form, 'message': message, 'filename': file})


def build_rvt_tables(request, wb, nextbatch):
    worksheets = ['vDisk', 'vPartition', 'vHost', 'vDatastore']

    for sht in worksheets:
        count = 0
        sh = wb.sheet_by_name(sht)
        for row in range(sh.nrows):
            if count == 0:
                #  grab the header row for top 100 columns
                hr = [None] * 100
                for x in range(0, 100):
                    try:
                        hr[x] = sh.cell(row, x).value
                    except:
                        pass

            else:
                if sht == "vDisk":
                    vmid_col = header_col_num(hr, "VM ID")
                    disk_col = header_col_num(hr, "Disk")
                    cap_col = header_col_num(hr, "Capacity MB")
                    dskm_col = header_col_num(hr, "Disk Mode")
                    thn_col = header_col_num(hr, "Thin")
                    ctl_col = header_col_num(hr, "Controller")
                    pth_col = header_col_num(hr, "Path")
                    ano_col = header_col_num(hr, "Annotation")

                    saverecord = RVTvDisk(
                        rvt_vd_user=request.user,
                        rvt_vi_batch=nextbatch,
                        rvt_vd_vmid=sh.cell(row, vmid_col).value,
                        rvt_vd_disk=sh.cell(row, disk_col).value,
                        rvt_vd_capacitymb=sh.cell(row, cap_col).value,
                        rvt_vd_diskmode=sh.cell(row, dskm_col).value,
                        rvt_vd_thin=str_to_bool(sh.cell(row, thn_col).value),
                        rvt_vd_controller=sh.cell(row, ctl_col).value,
                        rvt_vd_path=sh.cell(row, pth_col).value,
                        rvt_vd_annotation=sh.cell(row, ano_col).value,
                    )
                    saverecord.save()

                elif sht == "vPartition":
                    vmid_col = header_col_num(hr, "VM ID")
                    disk_col = header_col_num(hr, "Disk")
                    cap_col = header_col_num(hr, "Capacity MB")
                    con_col = header_col_num(hr, "Consumed MB")
                    fre_col = header_col_num(hr, "Free MB")
                    ano_col = header_col_num(hr, "Annotation")

                    saverecord = RVTvPartition(
                        rvt_vp_user=request.user,
                        rvt_vi_batch=nextbatch,
                        rvt_vp_vmid=sh.cell(row, vmid_col).value,
                        rvt_vp_disk=sh.cell(row, disk_col).value,
                        rvt_vp_capacitymb=sh.cell(row, cap_col).value,
                        rvt_vp_consumedmb=sh.cell(row, con_col).value,
                        rvt_vp_freemb=sh.cell(row, fre_col).value,
                        rvt_vp_annotation=sh.cell(row, ano_col).value,
                    )
                    saverecord.save()

                elif sht == "vDatastore":
                    name_col = header_col_num(hr, "Name")
                    type_col = header_col_num(hr, "Type")
                    vmcount_col = header_col_num(hr, "# VMs")
                    cap_col = header_col_num(hr, "Capacity MB")
                    prov_col = header_col_num(hr, "Provisioned MB")
                    used_col = header_col_num(hr, "In Use MB")
                    fre_col = header_col_num(hr, "Free MB")

                    saverecord = RVTvDatastore(
                        rvt_vs_user=request.user,
                        rvt_vi_batch=nextbatch,
                        rvt_vs_name=sh.cell(row, name_col).value,
                        rvt_vs_type=sh.cell(row, type_col).value,
                        rvt_vs_vmcount=sh.cell(row, vmcount_col).value,
                        rvt_vs_capacitymb=sh.cell(row, cap_col).value,
                        rvt_vs_provisioinedmb=sh.cell(row, prov_col).value,
                        rvt_vs_usedmb=sh.cell(row, used_col).value,
                        rvt_vs_freemb=sh.cell(row, fre_col).value,
                    )
                    saverecord.save()

                elif sht == "vHost":
                    host_col = header_col_num(hr, "Host")
                    dc_col = header_col_num(hr, "Datacenter")
                    clstr_col = header_col_num(hr, "Cluster")
                    cpu_col = header_col_num(hr, "CPU Model")
                    spd_col = header_col_num(hr, "Speed")
                    sock_col = header_col_num(hr, "# CPU")
                    ccore_col = header_col_num(hr, "Cores per CPU")
                    core_col = header_col_num(hr, "# Cores")
                    cpuper_col = header_col_num(hr, "CPU usage %")
                    mem_col = header_col_num(hr, "# Memory")
                    memper_col = header_col_num(hr, "Memory usage %")
                    vmcount_col = header_col_num(hr, "# VMs")
                    vmpc_col = header_col_num(hr, "VMs per Core")
                    vcpu_col = header_col_num(hr, "# vCPUs")
                    vcpc_col = header_col_num(hr, "vCPUs per Core")
                    vram_col = header_col_num(hr, "vRAM")
                    vmum_col = header_col_num(hr, "VM Used memory")
                    vmsm_col = header_col_num(hr, "VM Memory Swapped")
                    vmbm_col = header_col_num(hr, "VM Memory Ballooned")
                    cevc_col = header_col_num(hr, "Current EVC")
                    mevc_col = header_col_num(hr, "Max EVC")
                    ver_col = header_col_num(hr, "ESX Version")
                    boot_col = header_col_num(hr, "Boot time")

                    saverecord = RVTvHost(
                        rvt_vh_user=request.user,
                        rvt_vi_batch=nextbatch,
                        rvt_vh_hostname=sh.cell(row, host_col).value,
                        rvt_vh_datacenter=sh.cell(row, dc_col).value,
                        rvt_vh_cluster=sh.cell(row, clstr_col).value,
                        rvt_vh_cputype=sh.cell(row, cpu_col).value,
                        rvt_vh_speed=sh.cell(row, spd_col).value,
                        rvt_vh_socketcount=sh.cell(row, sock_col).value,
                        rvt_vh_socketcores=sh.cell(row, ccore_col).value,
                        rvt_vh_cores=sh.cell(row, core_col).value,
                        rvt_vh_cpu_usagepercent=sh.cell(row, cpuper_col).value,
                        rvt_vh_memorymb=sh.cell(row, mem_col).value,
                        rvt_vh_mem_usagepercent=sh.cell(row, memper_col).value,
                        rvt_vh_vmcount=sh.cell(row, vmcount_col).value,
                        rvt_vh_vmpercore=sh.cell(row, vmpc_col).value,
                        rvt_vh_vcpucount=sh.cell(row, vcpu_col).value,
                        rvt_vh_vcpupercore=sh.cell(row, vcpc_col).value,
                        rvt_vh_vram=sh.cell(row, vram_col).value,
                        rvt_vh_usedmem=sh.cell(row, vmum_col).value,
                        rvt_vh_swapmem=sh.cell(row, vmsm_col).value,
                        rvt_vh_balloonmem=sh.cell(row, vmbm_col).value,
                        rvt_vh_evc=sh.cell(row, cevc_col).value,
                        rvt_vh_maxevc=sh.cell(row, mevc_col).value,
                        rvt_vh_esxversion=sh.cell(row, ver_col).value,
                        rvt_vh_boottime=sh.cell(row, boot_col).value,
                    )
                    saverecord.save()

            count = count + 1

    return "Additional Tables, Processing Complete. "

def header_col_num(hr, srchstring):
    count = 0
    for cell in hr:
        if srchstring == cell:
            return count

        count=count+1


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError


def handle_uploaded_file(f, p):
    #  writefile =  'uploads/' + user.username + '/' + f.name
    #  get extension & give our file a unique name.
    ext = f.name.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    writefile = p + filename
    os.makedirs(os.path.dirname(writefile), exist_ok=True)
    with open(writefile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return filename


@login_required
def viewrvt(request, batchfilter=0):

    my_records = RVTvInfo.objects.records_for_user(request.user)

    if batchfilter == 0:
        my_batches = RVTvInfo.objects.batches(request.user)
        return render(request, "rvt/rvt_rvtbatchview.html",
                      {'records': my_records, 'batches': my_batches})

    else:
        my_records = RVTvInfo.objects.records_for_batch(request.user, batchfilter)
        my_vdisks = RVTvDisk.objects.records_for_batch(request.user, batchfilter)

        message = "%s %s" % ("Showing Data for Batch ", batchfilter)
        return render(request, "rvt/rvt_rvtdataview.html",
                      {'records': my_records, 'batch': batchfilter, 'message': message, 'vdisks': my_vdisks})


def delrvt(request, batchid):
    #this will implicitly only return matching records that you also OWN
    # - enforced in the model records_for_batch queryset
    # - so we don't need to enforce here
    my_records = RVTvInfo.objects.records_for_batch(request.user, batchid)

    if request.method == 'GET':
        return render(request, "rvt/rvt_rvtdata_confirm_delete.html", {'object': my_records})

    else:
        my_records = RVTvInfo.objects.records_for_batch(request.user, batchid)
        #  my_records.get(rvt_vi_batch=batchid)
        test = my_records.all()[:1].get()
        file = test.rvt_vi_filename
        os.remove(file)
        my_records.delete()
        return redirect('rvt_view')


#  ######################################################
#  ######################################################
#  CSV Processing Below - UNUSED - switched to XLS for RVT - keep for future
#
@login_required
def uploadcsv(request):

    #  not a file - show the form
    if request.method == 'GET':
        message = ""
        form = UploadFileForm()
        orgs = Org.objects.filter(org_creator_id=request.user)
        return render(request, "rvt/rvt_rvtdataform.html", {'form': form, 'orgs': orgs, 'message': message})

    # is a file - process & display
    else:
        file = request.FILES['file']
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if not file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('rvt_index')

            #  init the file read
            tfile = TextIOWrapper(file.file, encoding=request.encoding)
            reader = csv.reader(tfile)

            #  let's look up our highest batch number & increment to the next
            try:
                maxbatch = RVTvInfo.objects.order_by('-rvt_vi_batch',)[0]
                nextbatch = maxbatch.rvt_vi_batch + 1
            except:
                nextbatch = 1

            # look up provided ORG id:
            givenorg = Org.objects.get(id=request.POST['org'])

            count = 0
            for row in reader:
                if count > 0:
                    saverecord = RVTvInfo(
                        rvt_vi_user=request.user,
                        rvt_vi_org=givenorg,
                        rvt_vi_batch=nextbatch,
                        rvt_vi_filename=file,
                        rvt_vi_vm=row[0],
                        rvt_vi_powerstate=row[1],
                        rvt_vi_guest_state=row[2],
                        rvt_vi_provisioned_mb=row[3].replace(',', ''),
                        rvt_vi_in_use_mb=row[4].replace(',', ''),
                        rvt_vi_unshared_mb=row[5].replace(',', ''),
                    )
                    saverecord.save()

                else:
                    headervalues = row

                count = count + 1

            tfile.close()

            return redirect('rvt_view')

        else:
            message = "Form Validation Error! : FileName: "
            return render(request, "rvt/rvt_rvtdataform.html",
                          {'form': form, 'message': message, 'filename': file})
