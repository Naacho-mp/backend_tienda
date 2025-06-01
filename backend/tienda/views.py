from django.shortcuts import redirect, render, get_object_or_404
from tienda.models import Producto
from tienda.forms import ProductoForm
from django.forms import modelform_factory
from django.core.paginator import Paginator

#testing push
#puto el que lee
#hoal
#hoal2
#hoal3
ProductoForm = modelform_factory(Producto, exclude=[])


def mostrar_productos(request):
    productos = Producto.objects.all()

    items_por_pagina = request.GET.get('paginador', 12)

    page_number = request.GET.get('page')

    paginador = Paginator(productos, items_por_pagina)
    page_obj = paginador.get_page(page_number)

    return render(request, 'mostrar_productos.html', {'page_obj': page_obj,})



def agregar_producto(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES)

        if producto_form.is_valid():
            producto_form.save()
            return redirect('mostrar_productos')

    else:
        producto_form = ProductoForm()
        
    data = {'producto_form':producto_form}
    return render(request, "agregar_producto.html", data)


def actualizar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES, instance=producto)

        if producto_form.is_valid():
            producto_form.save()
            return redirect('mostrar_productos')

    else:
        producto_form = ProductoForm(instance=producto)

    data = {'producto_form': producto_form}
    return render(request, 'actualizar_producto.html', data)

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id) 

    
    
    producto.delete()
    return redirect('mostrar_productos')