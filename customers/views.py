from django.shortcuts import render, redirect
from .forms import CustomerForm
from .models import Customer
from django.http import HttpResponseRedirect
# Create your views here.
def customer_list(request,):

    customers = Customer.objects.all()

    context = {
        'customers': customers,
    }
    return render(request, 'customers/list.html', context)

def customer_detail(request,):
    if request.method == "POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
            }
            messages.success(request,' customer has been created')
            form.save()
        return redirect('customers:list')
            
    else:
        form=CustomerForm()
        context = {
            'form': form,
        }
    return render(request, 'customers/detail.html', context)
def customer_add(request):
    
    email = request.POST['email']
    customer = Customer(email = request.POST['email'])
    customer.save()
    return redirect('customers:list')

def customer_delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('customers:list')