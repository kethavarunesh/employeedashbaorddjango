from django.shortcuts import render, redirect, get_object_or_404
from .models import  Mtplnew_dataentry
from django.http import JsonResponse
from django.contrib import messages

def homepage(request):

    return render(request,'Home.html')

def create_document(request):
    if request.method == 'POST':
        empcode = request.POST.get('empcode')
        project_name = request.POST.get('project_name')
        date = request.POST.get('date')
        document_no = request.POST.get('document_no')
        order_serial_no = request.POST.get('order_serial_no')
        department = request.POST.get('department')
        material_code = request.POST.get('material_code')
        material_description = request.POST.get('material_description')
        supplier_name = request.POST.get('supplier_name')
        qty = request.POST.get('qty')
        value = request.POST.get('value')
        rejection_reason = request.POST.get('rejection_reason')
        reason_for_rejection = request.POST.get('reason_for_rejection')
        file_upload = request.FILES.get('file_upload')
        man_hours_wasted = request.POST.get('man_hours_wasted')
        machine_hours_wasted = request.POST.get('machine_hours_wasted')
        information_to_buyer = request.POST.get('information_to_buyer')

        Mtplnew_dataentry.objects.create(
            empcode=empcode,
            project_name=project_name,
            date=date,
            document_no=document_no,
            order_serial_no=order_serial_no,
            department=department,
            material_code=material_code,
            material_description=material_description,
            supplier_name=supplier_name,
            qty=qty,
            value=value,
            rejection_reason=rejection_reason,
            reason_for_rejection=reason_for_rejection,
            file_upload=file_upload,
            man_hours_wasted=man_hours_wasted,
            machine_hours_wasted=machine_hours_wasted,
            information_to_buyer=information_to_buyer
        )

        messages.success(request, 'Data saved successfully.')

        return redirect('create_document')
        
    return render(request, 'Entrypage.html')

def specific_empfilter(request):
    empcode = '987456' 
    
    documents = Mtplnew_dataentry.objects.filter(empcode=empcode)
    
    for document in documents:
        if document.status == 0:
            document.status_text = 'Pending at Hod'
        elif document.status == 1:
            document.status_text = 'Pending at PQA HOD'
        elif document.status == 3:
            document.status_text = 'Rejected by HOD'
        elif document.status == 11:
            document.status_text = 'Approved by PQA'
        elif document.status == 33:
            document.status_text = 'Rejected by PQA HOD'
        elif document.status == 111:
            document.status_text = 'Approved by Purchase'
        elif document.status == 333:
            document.status_text = 'Rejected by Purchase'
        elif document.status == 1111:
            document.status_text = 'Approved by Plant Head'
        elif document.status == 3333:
            document.status_text = 'Rejected by Plant Head'
        else:
            document.status_text = 'Other Status'
    context = {
        'documents': documents,
    }
    return render(request, 'specificemployee.html', context)

def employee_reports(request):
   
    documents = Mtplnew_dataentry.objects.all()

    for document in documents:
        if document.status == 0:
            document.status_text = 'Pending'
        elif document.status == 1:
            document.status_text = 'Pending at PQA HOD'
        elif document.status == 3:
            document.status_text = 'Rejected by HOD'
        elif document.status == 11:
            document.status_text = 'Approved by pqa'
        elif document.status == 33:
            document.status_text = 'Rejected by PQA HOD'
        elif document.status == 111:
            document.status_text = 'Approved by purchase'
        elif document.status == 333:
            document.status_text = 'Rejected by purchase'
        elif document.status == 1111:
            document.status_text = 'Approved by Plant Head'
        elif document.status == 3333:
            document.status_text = 'Rejected by Plant Head'
        else:
            document.status_text = 'Other Status'

    return render(request, 'reports.html', { 'documents': documents})

def edit_document(request, document_id):
    document = get_object_or_404(Mtplnew_dataentry, id=document_id)

    if request.method == 'POST':
        document.empcode = request.POST.get('empcode')
        document.project_name = request.POST.get('project_name')
        document.date = request.POST.get('date')
        document.document_no  = request.POST.get('document_no')
        document.order_serial_no = request.POST.get('order_serial_no')
        document.department = request.POST.get('department')
        document.material_code = request.POST.get('material_code')
        document.material_description = request.POST.get('material_description')
        document.supplier_name = request.POST.get('supplier_name')
        document.qty = request.POST.get('qty')
        document.value = request.POST.get('value')
        document.rejection_reason = request.POST.get('rejection_reason')
        document.reason_for_rejection = request.POST.get('reason_for_rejection')
        document.file_upload = request.FILES.get('file_upload')
        document.man_hours_wasted = request.POST.get('man_hours_wasted')
        document.machine_hours_wasted = request.POST.get('machine_hours_wasted')
        document.information_to_buyer = request.POST.get('information_to_buyer')
        document.status = 0
        document.planthod_remarks=""
        document.purchase_remarks=""
        document.approval_comment=""
        document.ncraised=""
        document.save()
        messages.success(request, 'Data updated successfully.')
        return redirect('edit_document', document_id=document.id) 

    return render(request, 'edit.html', {'document': document})

def hoddashbaord(request):
    documents = Mtplnew_dataentry.objects.filter(status=0) 
    return render(request, 'hoddashboard.html', {'documents': documents})

def hod_approve_document(request, document_id):
    document = get_object_or_404(Mtplnew_dataentry, pk=document_id)
    document.status = 1 
    document.save()
    return JsonResponse({'success': True})

def hod_reject_document(request, document_id):
    document = get_object_or_404(Mtplnew_dataentry, pk=document_id)
    document.status = 3 
    document.save()
    return JsonResponse({'success': True})
   
   
def pqa_dashboard(request):
    documents = Mtplnew_dataentry.objects.filter(status=1) 
    return render(request, 'pqa_dashboard.html', {'documents': documents})

def pqa_approve_document(request, document_id):
    if request.method =="POST":
     document = get_object_or_404(Mtplnew_dataentry, id=document_id)
    approval_comment = request.POST.get('approval_comment')
    ncraised = request.POST.get('ncraised')
    print(approval_comment)
    print(ncraised)
    document.status = 11  
    document.approval_comment = approval_comment
    document.ncraised = ncraised
    document.save()
    return JsonResponse({'success': True})

def pqa_reject_document(request, document_id):
    document = get_object_or_404(Mtplnew_dataentry, id=document_id)
    document.status = 33  
    document.save()
    return JsonResponse({'success': True})

def purchasehod_dashboard(request):
    documents = Mtplnew_dataentry.objects.filter(status=11) 
    return render(request, 'purchase_hod.html', {'documents': documents})


def purchase_approve_document(request, document_id):
   if request.method =="POST":
     document = get_object_or_404(Mtplnew_dataentry, id=document_id)
     purchase_remarks = request.POST.get('remarks')
     print(purchase_remarks)
     document.status = 111
     document.purchase_remarks = purchase_remarks
     document.save()
     return JsonResponse({'success': True})


def purchase_reject_document(request, document_id):
   if request.method =="POST":
     document = get_object_or_404(Mtplnew_dataentry, id=document_id)
     purchase_remarks = request.POST.get('remarks1')
     print(purchase_remarks)
     document.status = 333
     document.purchase_remarks = purchase_remarks
     document.save()
     return JsonResponse({'success': True})
   
def planthead(request):
  
    documents = Mtplnew_dataentry.objects.filter(status=111) 
    return render(request, 'planthod.html', {'documents': documents})   
   
def planthead_approve_document(request, document_id):
    document = get_object_or_404(Mtplnew_dataentry, id=document_id)
    planthod_remarks = request.POST.get('remarks')
    print(planthod_remarks)
    document.status = 1111 
    document.planthod_remarks = planthod_remarks
    document.save()
    return JsonResponse({'success': True}) 

def planthead_reject_document(request, document_id):
    document = get_object_or_404(Mtplnew_dataentry, id=document_id)
    planthod_remarks = request.POST.get('remarks1')
    print(planthod_remarks)
    document.status = 3333
    document.planthod_remarks = planthod_remarks
    document.save()
    return JsonResponse({'success': True}) 



