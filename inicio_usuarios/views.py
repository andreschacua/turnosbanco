from django.shortcuts import render, redirect
from django.http import HttpResponse
from inicio_usuarios.models import Clientes, Turnos, TurnosPasados
from django.urls import reverse

def inicio_usuarios(request):
    return render(request, "index.html")

def comparar(request):
    cedula = request.GET.get("cedula", "")
    
    if cedula:
        clientes = Clientes.objects.filter(cedula__exact=cedula)
        if clientes.exists():
            return redirect(reverse('asignar_turno') + f'?cedula={cedula}')
        else:
            return redirect(reverse('registro_cliente', kwargs={'cedula': cedula}))
    
    return render(request, "resultados_busqueda.html", {"clientes": [], "query": cedula})

def asignar_turno(request):
    cedula = request.GET.get('cedula')
    if request.method == 'POST':
        turno_tipo = None
        if 'caja' in request.POST:
            turno_tipo = 'C'
        elif 'asesor' in request.POST:
            turno_tipo = 'A'
        elif 'gerencia' in request.POST:
            turno_tipo = 'G'
        
        if turno_tipo:
            ultimo_turno = Turnos.objects.filter(turno__startswith=turno_tipo).order_by('turno').last()
            if ultimo_turno:
                ultimo_numero = int(ultimo_turno.turno[1:])
                nuevo_numero = ultimo_numero + 1
            else:
                nuevo_numero = 1
            nuevo_turno = f'{turno_tipo}{nuevo_numero:03d}'
            Turnos.objects.create(cedula=cedula, turno=nuevo_turno)
            return HttpResponse(f'Turno asignado: {nuevo_turno}')
    
    return render(request, 'asignar_turno.html', {'cedula': cedula})

def registro_cliente(request, cedula):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        if nombre and telefono:
            nuevo_cliente = Clientes(nombre=nombre, cedula=cedula, telefono=telefono)
            nuevo_cliente.save()
            return redirect(reverse('asignar_turno') + f'?cedula={cedula}')
    return render(request, 'registro_cliente.html', {'cedula': cedula})

def agregar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        if nombre and cedula and telefono:
            nuevo_cliente = Clientes(nombre=nombre, cedula=cedula, telefono=telefono)
            nuevo_cliente.save()
            return redirect('ver_clientes')
    return render(request, 'agregar_cliente.html')
