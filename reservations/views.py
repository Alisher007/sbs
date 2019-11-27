from django.shortcuts import render
from .forms import ReservationForm
from .models import Reservation, Avail, Table, Timestart
from datetime import date
from .utils import Test, get_or_none
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib import messages

def home(request,):
    return render(request, 'home.html')

def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            instance = form.save()
            res_id = int(instance.pk)
            availTemp = []
            for avail in Test.avail:
                availTemp.append(Avail(name=avail,reservation_id=res_id,date=instance.date))
            Avail.objects.bulk_create(availTemp)
            Test.avail = []
            return redirect('reservation:list')
        else:
            return HttpResponseRedirect(request.path_info)
    else:
        form = ReservationForm()
    return render(request,'reservation/reservation_create.html', {'form': form})

def reservation_update(request):
    next2 = request.GET.get('next')
    if request.GET.get('next'):
        print('nexttttttttt')
        print(request.GET.get('next'))
    if request.method == 'POST':
        Test.res_id = request.POST.get('res_id')
        date2 = request.POST.get('date')
        if Test.res_id != '':
            messagesNote = Test.res_id + ' is modified'
            reserve_detail = get_or_none(Reservation, id=Test.res_id)
            form = ReservationForm(request.POST or None , instance=reserve_detail)
            print('   form update ')
        else:
            messagesNote = 'Reservation  is created'
            form = ReservationForm(request.POST)
            print('   form  ')
        if form.is_valid():
            print('   form.is_valid()  ')
            instance = form.save()
            res_id = int(instance.pk)
            availTemp = []
            if Test.res_id != '':
                Avail.objects.filter(reservation_id=Test.res_id).delete()
            for avail in Test.avail:
                availTemp.append(Avail(name=avail,reservation_id=res_id,date=instance.date))
            Avail.objects.bulk_create(availTemp)
            Test.res_id = ''
            Test.avail = []
            messages.success(request,messagesNote)
            date2 = str(instance.date)
            return redirect('reservation:list_date', date=date2)
        else:
            print('   not form.is_valid()  ')
            Test.res_id = ''
            Test.avail = []
            messages.info(request,'could not modify or create reservation ')
            return redirect('reservation:list_date', date=date2)
    else:
        reserve_detail = []
        time_id = request.GET.get('time_id')
        date2 = request.GET.get('date')
        table_id = request.GET.get('table_id')
        if request.GET.get('res_id'):
            res_id = request.GET.get('res_id')
            reserve_detail = list(Reservation.objects.filter(id=res_id))
        if reserve_detail != []:
            form=ReservationForm(
                initial={
                    "table":table_id,
                    "customer":reserve_detail[0].customer,
                    "timestart":reserve_detail[0].timestart_id,
                    "duration":reserve_detail[0].duration,
                    "product":reserve_detail[0].product,
                    "date":date2,})
            context = {
                "res_id":res_id,
                'form': form,
            }
        else:
            form=ReservationForm(
                initial={
                    "table":table_id,
                    "timestart":time_id,
                    "duration":'15',
                    "date":date2,}
            )
            context = {
                'form': form,
            }
        return render(request, 'reservation/reservation_detail.html', context)
    return redirect('reservation:list')

def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation/reservation_list.html',{'reservations':reservations})

def reservation_detail(request):
    reserve_detail = []
    time_id = request.GET.get('time_id')
    date2 = request.GET.get('date')
    table_id = request.GET.get('table_id')
    if request.GET.get('res_id'):
        res_id = request.GET.get('res_id')
        reserve_detail = list(Reservation.objects.filter(id=res_id))
    if reserve_detail != []:
        form=ReservationForm(
            initial={
                "table":table_id,
                "customer":reserve_detail[0].customer,
                "timestart":reserve_detail[0].timestart_id,
                "duration":reserve_detail[0].duration,
                "product":reserve_detail[0].product,
                "date":date2,})
        context = {
            "res_id":res_id,
            'form': form,
        }
    else:
        form=ReservationForm(
            initial={
                "table":table_id,
                "timestart":time_id,
                "duration":'15',
                "date":date2,}
        )
        context = {
            'form': form,
        }
    return render(request, 'reservation/reservation_detail.html', context)

def reservation_list2(request,):
    today_ = str(date.today())
    if request.GET.get('date'):
        today_ = request.GET.get('date')
    # getting the reservations for selected date
    res = list(Avail.objects.filter(date=today_).select_related('reservation'))
    table = list(Table.objects.all())
    time_list = list(Timestart.objects.all())
    # creating availibility table
    avail_list = [[{
        'table':str(ta),'table_id':ta.id,'time':str(ti),'time_id':ti.id, 'status':'vacant'
        } for ta in table] for ti in time_list]

    # inserting queryset data into availability table
    if res:
        for avail_list1 in avail_list:
            for avail_list2 in avail_list1:
                for re in res:
                    if re.name == today_ + '_' + avail_list2.get('time') + '_' + str(avail_list2.get('table')):
                        avail_list2.update({
                        'table':avail_list2.get('table'),
                        'time':avail_list2.get('time'), 
                        'customer': re.reservation,
                        'res_id':re.reservation_id,
                        'status':'' ,
                        'occupied':'occupied'})
    context = {
        'avail': avail_list,
        'table': table,
        'date': today_,
    }
    return render(request, 'reservation/reservation_list2.html', context)

def reservation_list_date(request,date):
    today_ = date
    if request.GET.get('date'):
        today_ = request.GET.get('date')
    res = list(Avail.objects.filter(date=today_).select_related('reservation'))
    table = list(Table.objects.all())
    time_list = list(Timestart.objects.all())
    # creating availibility table
    avail_list = [[{
        'table':str(ta),'table_id':ta.id,'time':str(ti),'time_id':ti.id, 'status':'vacant'
        } for ta in table] for ti in time_list]

    # inserting queryset data into availability table
    if res:
        for avail_list1 in avail_list:
            for avail_list2 in avail_list1:
                for re in res:
                    if re.name == today_ + '_' + avail_list2.get('time') + '_' + str(avail_list2.get('table')):
                        avail_list2.update({
                        'table':avail_list2.get('table'),
                        'time':avail_list2.get('time'), 
                        'customer': re.reservation,
                        'res_id':re.reservation_id,
                        'status':'' ,
                        'occupied':'occupied'})
    context = {
        'avail': avail_list,
        'table': table,
        'date': today_,
    }
    return render(request, 'reservation/reservation_list2.html', context)

def reservation_delete(request):
    if request.method == "POST":
        res_id = request.POST.get('res_id')
        if res_id:
            item_to_delete = Reservation.objects.get(id=res_id)
            messages.success(request, str(item_to_delete.customer) +' is deleted.')
            date2 = item_to_delete.date
            item_to_delete.delete()
            Avail.objects.filter(reservation_id=res_id).delete()
            return redirect('reservation:list_date', date=date2)