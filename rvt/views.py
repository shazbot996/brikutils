from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import DeleteView, UpdateView, ListView
from django.urls import reverse_lazy

#  form & models
from .forms import UploadFileForm, OrgForm
from .models import RVTvInfo
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

            path = 'uploads/' + request.user.username + '/'

            file_uuid = handle_uploaded_file(request.user, file, path)

            #  init the file read - XLS focused here
            wb = xlrd.open_workbook(path + file_uuid)
            sh = wb.sheet_by_name('vInfo')
            num_rows = sh.nrows

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

            for rownum in range(sh.nrows):
                if count > 0:
                    saverecord = RVTvInfo(
                        rvt_vi_user=request.user,
                        rvt_vi_assessment=linked_assessment,
                        rvt_vi_batch=nextbatch,
                        rvt_vi_filename=path + file_uuid,
                        rvt_vi_vm=sh.cell(rownum, 0).value,
                        rvt_vi_powerstate=sh.cell(rownum, 1).value,
                        rvt_vi_guest_state=sh.cell(rownum, 2).value,
                        rvt_vi_provisioned_mb=sh.cell(rownum, 3).value,
                        rvt_vi_in_use_mb=sh.cell(rownum, 4).value,
                        rvt_vi_unshared_mb=sh.cell(rownum, 5).value,  #removed .replace(',', '') from original csv processing
                    )
                    saverecord.save()
                count = count + 1


            topmessage = "%s.%s" % (sh.nrows, ' Records Added!')
            messages.error(request, topmessage)

            return redirect('rvt_view')

        else:
            message = "Form Validation Error! : FileName: "
            return render(request, "rvt/rvt_rvtdataform.html",
                          {'form': form, 'message': message, 'filename': file})


def handle_uploaded_file(user, f, p):
    #  writefile =  'uploads/' + user.username + '/' + f.name
    #  get extension & give our file a unique name.
    ext = f.name.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    writefile = p + filename
    #  writefile = f.name = "%s.%s" % (uuid.uuid4(), ext)
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
        message = ""
        return render(request, "rvt/rvt_rvtbatchview.html",
                      {'records': my_records, 'batches': my_batches, 'message': message})

    else:
        my_records = RVTvInfo.objects.records_for_batch(request.user, batchfilter)

        message = "%s %s" % ("Showing Data for Batch ", batchfilter)
        return render(request, "rvt/rvt_rvtdataview.html",
                      {'records': my_records, 'batch': batchfilter, 'message': message})


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
