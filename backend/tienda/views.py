from django.shortcuts import redirect, render, get_object_or_404
from tienda.models import Producto, Categoria
from tienda.forms import ProductoForm, CategoriaForm
from django.forms import modelform_factory
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST


ProductoForm = modelform_factory(Producto, exclude=[])
CategoriaForm = modelform_factory(Categoria, exclude=[])


########################## CRUD PRODUCTO ###################################

def mostrar_productos(request):
    productos = Producto.objects.all()

    items_por_pagina = request.GET.get('paginador', 12)

    page_number = request.GET.get('page')

    paginador = Paginator(productos, items_por_pagina)
    page_obj = paginador.get_page(page_number)

    return render(request, 'mostrar_productos.html', {'page_obj': page_obj,})



def ver_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'ver_producto.html', {'producto': producto})



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

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    cantidad = int(request.POST.get('cantidad', 1))

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += cantidad
    else:
        carrito[str(producto_id)] = cantidad

    request.session['carrito'] = carrito
    return redirect('ver_producto', producto_id=producto_id)

def ver_carrito(request):
    carrito = request.session.get('carrito', {})

    productos = Producto.objects.filter(id__in=carrito.keys())

    carrito_detalle = []
    total = 0 
    for producto in productos:
        cantidad = carrito[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal  

        carrito_detalle.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })
    return render(request, 'ver_carrito.html', {
        'carrito': carrito_detalle,
        'total': total  
    })


@require_POST
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]

    request.session['carrito'] = carrito
    return redirect('ver_carrito')



########################## CRUD CATEGORIA ####################################

def mostrar_categorias(request):
    categorias = Categoria.objects.all()
    data = {"categorias":categorias}

    return render (request, "mostrar_categorias.html", data)

def agregar_categoria(request):
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST, request.FILES)

        if categoria_form.is_valid():
            categoria_form.save()
            return redirect('mostrar_categorias')

    else:
        categoria_form = CategoriaForm()
        
    data = {'categoria_form':categoria_form}
    return render(request, "agregar_categoria.html", data)


def actualizar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)

    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST, request.FILES, instance=categoria)

        if categoria_form.is_valid():
            categoria_form.save()
            return redirect('mostrar_categorias')

    else:
        categoria_form = CategoriaForm(instance=categoria)

    data = {'categoria_form': categoria_form}
    return render(request, 'actualizar_categoria.html', data)



def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id) 

    categoria.delete()
    return redirect('mostrar_categorias')

