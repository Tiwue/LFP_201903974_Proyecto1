from tkinter.filedialog import askopenfilename
from tkinter import Tk
from tkinter import filedialog
from generarMenu import getDatos
from generarFactura import getdatos
from generarMenu import limpiar
from generarFactura import Limpiar

def cargaMenu():
    
    limpiar()
    ventana=Tk()
    try:    
        ventana.filename = filedialog.askopenfilename()
        archivo=open(ventana.filename,"r",encoding="utf-8")
        entrada = archivo.read()
        getDatos(entrada)
        archivo.close()    
    except:
        print("No fue posible leer el archivo")    
    
    ventana.destroy()

def cargaPedido():
    Limpiar()
    ventana=Tk()
    try:
        ventana.filename = filedialog.askopenfilename()
        archivo=open(ventana.filename,"r",encoding="utf-8")
        entrada = archivo.read()
        getdatos(entrada)
        archivo.close()
    except:
        print("No fue posible leer el archivo")
    ventana.destroy() 