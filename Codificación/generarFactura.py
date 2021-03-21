import re
from tokens import Token
from error import  Error
from platillo import Platillo
from menu import Menu
from generarMenu import platillos
from pedido import Pedido
from factura import Factura
import datetime
from dateutil.relativedelta import relativedelta

import os
lineasPedido=""
errores=[]
tokens=[]
identificadores=[]
nombre=""
nit=""
direccion=""
porcentaje=None
total=0
pedidos=[]
factura=None
productos=platillos
NoFac=0
def getdatos(linea):
    global lineasPedido
    lineasPedido=linea

def Analisis():
    global productos,lineasPedido,errores,tokens,identificadores,nombre,direccion,porcentaje,total,nit,pedidos,factura,NoFac

    numero_token=0
    numero_error=0
    fila=1
    estado=0
    lexema=""
    columna=0
    current_cantidad=""
    current_id=""
    if lineasPedido != "":
        for caracter in lineasPedido:
                columna +=1
                if estado==0:
                    if caracter =="\n":
                        fila+=1
                        columna=1
                        estado=0
                    elif caracter==" ":
                        continue
                    elif caracter=="":
                        continue
                    elif caracter == "'":
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                        estado = 1
                    elif re.search(r"[1-9]",caracter):
                        lexema +=caracter
                        estado=13
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido"))
                        lexema += caracter
                elif estado==1:
                    if re.search(r"[a-zA-Z\s]",caracter):
                        lexema += caracter
                        estado=2
                    else:
                        numero_error+=1
                        
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido en nombre"))
                elif estado==2:
                    if re.search(r"[a-zA-Z\s]",caracter):
                        lexema +=caracter
                        continue
                    elif caracter=="'":
                        numero_token+=1
                        nombre=lexema.strip()
                        tokens.append(Token(numero_token,nombre,fila,columna-1,"TK_cadena"))
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                        lexema=""
                        estado=3
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido en nombre"))
                        
                elif estado==3:
                    if caracter==" ":
                        continue
                    elif caracter==",":
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_coma"))
                        estado=4
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba ,"))
                
                elif estado==4:
                    if caracter==" ":
                        continue
                    elif caracter=="'":
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                        estado=5
                    else:   
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba '"))

                elif estado==5:
                    if caracter==" ":
                        continue
                    elif re.search(r"[0-9-]",caracter):
                        lexema+=caracter
                        continue
                    elif caracter=="'":
                        numero_token+=1
                        nit=lexema.strip()
                        tokens.append(Token(numero_token,lexema,fila,columna-1,"TK_nit"))
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                        lexema=""
                        estado=6
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido"))
                elif estado==6:
                    if caracter==" ":
                        continue
                    elif caracter==",":
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_coma"))
                        estado=7
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba ,"))
                elif estado==7:
                    if caracter==" ":
                        continue
                    elif caracter=="'":
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                        estado=8
                    else: 
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido se esperaba "))

                elif estado==8:
                    if re.search(r"[a-zA-Z\s0-9-.,]",caracter):
                        lexema+=caracter
                        continue
                    elif caracter=="'":
                        numero_token+=1
                        direccion=lexema.strip()
                        tokens.append(Token(numero_token,direccion,fila,columna-1,"TK_cadena"))
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                        lexema=""
                        estado=9
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido"))
                elif estado==9:
                    if caracter==" ":
                        continue
                    elif caracter==",":
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_coma"))
                        estado=10
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba ,"))
                elif estado==10:
                    if caracter==" ":
                        continue
                    elif re.search(r"[0-9]",caracter):
                        lexema+=caracter
                        estado=11
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Se esperaba un valor numerico"))
                elif estado==11:
                    if re.search(r"[0-9]",caracter):
                        lexema+=caracter
                    elif caracter=="%":
                        if float(lexema) <= 100:
                            if porcentaje != 0:
                                porcentaje=float(lexema)
                                numero_token+=1
                                tokens.append(Token(numero_token,porcentaje,fila,columna-1,"TK_porcentaje"))
                            else:
                                numero_error+=1
                                errores.append(Error(numero_error,fila,columna-1,lexema,"Solo puede haber un porcentaje por factura"))    
                        else:
                            numero_error+=1
                            errores.append(Error(numero_error,fila,columna-1,lexema,"El porcentaje debe ser menor al 100%"))
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_porcentaje"))
                        lexema=""
                        estado=0

                elif estado==13:
                    if caracter==" ":
                        continue
                    elif re.search(r"[0-9]",caracter):
                        lexema+=caracter
                    elif caracter==",":
                        numero_token+=1
                        current_cantidad=int(lexema.strip())
                        tokens.append(Token(numero_token,current_cantidad,fila,columna-1,"TK_numero"))
                        numero_token+=1
                        tokens.append(Token(numero_token,caracter,fila,columna,"TK_coma"))
                        lexema=""
                        estado=14
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila, columna,caracter,"Caracter invalido"))
            
                elif estado==14:
                    
                    if caracter==" ":
                        continue 
                    elif re.search(r"[a-z]",caracter):
                        lexema+=caracter
                        estado=15
                    else:
                        numero_error+=1
                        errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, solo se permiten letras minuscilas en los identificadores"))
                elif estado==15:
                    if re.search(r"[a-z_0-9]",caracter):
                        lexema+=caracter
                    elif caracter=="\n":
                        current_id=lexema.strip()
                        numero_token+=1        
                        tokens.append(Token(numero_token,lexema.strip(),fila,columna-1,"TK_identificador"))
                        lexema=""
                        id_esist=False
                        for objeto in productos:
                            if objeto.identificador==current_id:
                                id_esist=True
                                
                            else:
                                continue        

                        if id_esist==True:
                            for objeto in productos:
                                if current_id==objeto.identificador:
                                    costo=float(objeto.precio)*float(current_cantidad)
                                    name=objeto.nombre
                                    price=objeto.precio
                                    pedidos.append(Pedido(current_cantidad,current_id,name,costo,price))
                        else:
                            numero_error+=1
                            errores.append(Error(numero_error,fila,columna-1,current_id,"Este producto no esta registrado en el menu")) 
                        estado=0
                        fila+=1
                        columna=0
                    elif caracter==" ":
                        current_id=lexema.strip()
                        numero_token+=1        
                        tokens.append(Token(numero_token,lexema.strip(),fila,columna-1,"TK_identificador"))
                        lexema=""
                        id_esist=False
                        for objeto in productos:
                            if objeto.identificador==current_id:
                                id_esist=True
                                
                            else:
                                continue        

                        if id_esist==True:
                            for objeto in productos:
                                if current_id==objeto.identificador:
                                    costo=float(objeto.precio)*float(current_cantidad)
                                    name=objeto.nombre
                                    price=objeto.precio
                                    pedidos.append(Pedido(current_cantidad,current_id,name,costo,price))
                        else:
                            numero_error+=1
                            errores.append(Error(numero_error,fila,columna-1,current_id,"Este producto no esta registrado en el menu")) 
                        estado=0                            


        current_id=lexema.strip()            
        numero_token+=1        
        tokens.append(Token(numero_token,lexema.strip(),fila,columna-1,"TK_identificador"))
        lexema=""
    
        id_esist=False
        for objeto in productos:
            if objeto.identificador==current_id:
                id_esist=True
            else:
                continue        

        if id_esist==True:
                for objeto in productos:
                    if current_id==objeto.identificador:
                        costo=float(objeto.precio)*float(current_cantidad)
                        name=objeto.nombre
                        price=objeto.precio
                        pedidos.append(Pedido(current_cantidad,current_id,name,costo,price)) 
        else:
                numero_error+=1
                errores.append(Error(numero_error,fila,columna-1,current_id,"Este producto no esta registrado en el menu"))        
        subtotal=0
        for objeto in pedidos:
            subtotal += objeto.costo
        propina= float(subtotal)*(porcentaje/100)
        total=float(subtotal)+propina
        one_year_from_now = datetime.datetime.now()
        fecha=one_year_from_now.strftime("%d/%m/%Y")
        NoFac+=1
        if errores==[]:
            factura=Factura(nombre,nit,direccion,pedidos,total,propina,porcentaje,fecha,NoFac,float(subtotal))
            generarFacturaHTML(factura)
            generarTokensHTML(tokens) 
        else:
            generarErroresHTML(errores)
            generarTokensHTML(tokens) 
    else:
        print("Debe generar un menu y cargar un archivo de pedido ")           



def generarFacturaHTML(factura):
    inicio="<!doctype html><html><head> <title>Factura</title> </head><body><h1 style=\"text-align: center;\">Factura No."+str(factura.no)+"""</h1>
    <h2 style=\"text-align: center;\">Fecha: """+factura.fecha+"""</h2><p style=\"text-align: center;\">&nbsp;</p>
    <p style=\"text-align: left; padding-left: 600px;\"><strong>Datos del Cliente:</strong></p><p style=\"text-align: left; padding-left: 600px;\"><strong>Nombre:</strong>"""+factura.cliente+"""</p>
    <p style=\"text-align: left; padding-left: 600px;\"><strong>NIT:</strong> """+factura.nit+"""</p><p style=\"text-align: left; padding-left: 600px;\"><strong>Direcci&oacute;n:</strong> """+factura.direccion+"""</p>
    <p style=\"text-align: left; padding-left: 600px;\"><strong>Descripci&oacute;n:</strong></p>
    <table style=\"border-collapse: collapse; border-color: white; margin-left: auto; margin-right: auto; height: 95px; width: 495px;\"><tbody><tr style=\"height: 23px;\"><td style=\"width: 78px; height: 23px; border-style: solid; text-align: center;\"><strong>Cantidad</strong></td>
    <td style=\"width: 191px; height: 23px; border-style: solid; text-align: center;\"><strong>Concepto&nbsp;</strong></td><td style=\"width: 101px; height: 23px; border-style: solid; text-align: center;\"><strong>Precio</strong></td><td style=\"width: 112px; height: 23px; border-style: solid; text-align: center;\"><strong>Total</strong></td></tr>"""
    mitad=""
    for element in factura.pedidos:
        mitad=mitad+"""<tr style="height: 18px;">
        <td style="width: 78px; height: 18px; border-color: black; border-style: solid; text-align: center;">"""+str(element.cantidad)+"""</td>
        <td style="width: 191px; height: 18px; border-color: black; border-style: solid; text-align: center;">"""+element.nombre+"""</td>
        <td style="width: 101px; height: 18px; border-color: black; border-style: solid; text-align: center;">"""+"Q"+str(element.precio)+"""</td>
        <td style="width: 112px; height: 18px; border-color: black; border-style: solid; text-align: center;">"""+"Q"+str(element.costo)+"""</td>
        </tr>"""
    subtotal="<tr style=\"height: 18px;\"><td style=\"width: 78px; height: 18px; text-align: center;\">&nbsp;</td><td style=\"width: 191px; height: 18px;\">&nbsp;</td><td style=\"width: 101px; height: 18px; text-align: center;\">Subtotal</td><td style=\"width: 112px; height: 18px; text-align: center;\">Q"+str(factura.subtotal)+"</td></tr>"
    propina="<tr style=\"height: 18px;\"><td style=\"width: 78px; height: 18px; text-align: center;\">&nbsp;</td><td style=\"width: 191px; height: 18px;\">&nbsp;</td><td style=\"width: 101px; height: 18px; text-align: center;\">Propina</td><td style=\"width: 112px; height: 18px; text-align: center;\">Q"+str(factura.propina)+"</td></tr>"
    total="<tr style=\"height: 18px;\"><td style=\"width: 78px; height: 18px; text-align: center;\">&nbsp;</td><td style=\"width: 191px; height: 18px;\">&nbsp;</td><td style=\"width: 101px; height: 18px; text-align: center;\"><strong>Total</strong></td><td style=\"width: 112px; height: 18px; text-align: center;\"><strong>Q"+str(factura.total)+"</strong></td></tr>"
    fin="</tbody></table></body> </html>"
    cadena=inicio+mitad+subtotal+propina+total+fin
    archivo=open('Factura.html','w',encoding="utf-8")
    archivo.write(cadena)
    archivo.close()
    os.system('Factura.html')
    print("Factura generada con exito")               
    
def generarErroresHTML(errores):
    inicio="<!doctype html><html><head> <title>Errores Factura</title> </head><body><h1 style=\"text-align: center; color: #3f7320;\">Errores:</h1> <table border=\"1\" align=\"center\" style=\"background-color:#ffffcc;border-collapse:collapse;border:1px solid #ffcc00\"><thead><tr><td><span style=\"color: #c82828;\">No.</span></td><td><span style=\"color: #c82828;\">Fila</span></td><td><span style=\"color: #c82828;\">Columna</span></td><td><span style=\"color: #c82828;\">Caracter</span></td><td><span style=\"color: #c82828;\">Descripción</span></td></tr></thead><tbody>"
    mitad=""
    for element in errores:
        mitad=mitad+"<tr><td>"+str(element.numero)+"</td><td>"+str(element.fila)+"</td><td>"+str(element.columna)+"</td><td>"+str(element.caracter)+"</td><td>"+str(element.descripcion)+"</td></tr>"
    fin="</tbody></table>"
    cadena=inicio+mitad+fin
    archivo=open('ErroresFactura.html','w',encoding="utf-8")
    archivo.write(cadena)
    archivo.close()
    os.system('ErroresFactura.html')
    print("Tabla de Errores generada con exito")

def generarTokensHTML(tokens):
    inicio="<!doctype html><html><head> <title>Tokens Factura</title> </head><body><h1 style=\"text-align: center; color: #3f7320;\">Tokens:</h1> <table border=\"1\" align=\"center\" style=\"background-color:#ffffcc;border-collapse:collapse;border:1px solid #ffcc00\"><thead><tr><td><span style=\"color: #c82828;\">No.</span></td><td><span style=\"color: #c82828;\">Lexema</span></td><td><span style=\"color: #c82828;\">Fila</span></td><td><span style=\"color: #c82828;\">Columna</span></td><td><span style=\"color: #c82828;\">Token</span></td></tr></thead><tbody>"
    mitad=""
    for element in tokens:
        mitad=mitad+"<tr><td>"+str(element.numero)+"</td><td>"+str(element.lexema)+"</td><td>"+str(element.fila)+"</td><td>"+str(element.columna)+"</td><td>"+str(element.descripcion)+"</td></tr>"
    fin="</tbody></table>"
    cadena=inicio+mitad+fin
    archivo=open('TokensFactura.html','w',encoding="utf-8")
    archivo.write(cadena)
    archivo.close()
    os.system('TokensFactura.html')
    print("Tabla de Tokens generada con exito")

def Limpiar():
    global lineasPedido,errores,tokens,nombre,nit,direccion,porcentaje,total,pedidos,factura
    lineasPedido=""
    errores.clear()
    tokens.clear()
    identificadores.clear()
    nombre=""
    nit=""
    direccion=""
    porcentaje=None
    total=0
    pedidos.clear()
    factura=None  
         