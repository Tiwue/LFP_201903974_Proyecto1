from pip._vendor.distlib.compat import raw_input
from cargas import cargaMenu
from cargas import cargaPedido
from generarMenu import analisis
from generarFactura import Analisis
from generarMenu import generarArbol
on=True
eleccion=1

while on==True:
    print("\t\t Proyecto 1- LFP")
    print("Lenguajes Formales - Steven Josue González Monroy")
    print("1.Cargar Menu")
    print("2.Cargar Orden")
    print("3.Generar Menu")
    print("4.Generar Factura")
    print("5.Generar Arbol")
    print("6.Salir\n")
    print("Ingrese una opcion:")

    eleccion=input()

    if int(eleccion)== 1:
        cargaMenu()
        print("Archivo leido con exito")
        raw_input("\nPresiona la tecla Enter para continuar")
    elif int(eleccion)==2:
        cargaPedido()
        print("Archivo leido con exito")
        raw_input("\nPresiona la tecla Enter para continuar")
    elif int(eleccion) == 3:
        analisis()
        raw_input("\nPresiona la tecla Enter para continuar")
    elif int(eleccion)==4:
        Analisis()
        raw_input("\nPresiona la tecla Enter para continuar")
    elif int(eleccion) == 5:
        generarArbol()
        raw_input("\nPresiona la tecla Enter para continuar")
    elif int(eleccion) == 6:
        print("Cerrando programa...")
        on = False
    else:
        print("Debe elegir una opcion valida")
        raw_input("\nPresiona la tecla Enter para continuar")            
