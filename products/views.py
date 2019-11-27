from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.http import HttpResponseRedirect
# Create your views here.
def product_list(request,):

    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'products/list.html', context)

def product_detail(request,):
    if request.method == "POST":
        form=ProductForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
            }
            messages.success(request,' product has been created')
            form.save()
        return redirect('products:list')
            
    else:
        form=ProductForm()
        context = {
            'form': form,
        }
    return render(request, 'products/detail.html', context)
def product_add(request):
    product = Product(name = request.POST['name'])
    product.save()
    return redirect('products:list')

def product_delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products:list')