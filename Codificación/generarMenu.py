
import re
from tokens import Token
from error import  Error
from platillo import Platillo
from menu import Menu
from graphviz import Source
import os
lineasMenu=""
errores=[]
tokens=[]
platillos=[]
reservada=""
nombre=""
categorias=[]
menu=None
identificadores=[]

def getDatos(linea):
    global lineasMenu
    lineasMenu=linea

def analisis():
    global lineasMenu, nombre, errores,tokens,platillos,reservada,nombre,categorias,menu,identificadores
    numero_token=0
    numero_error=0
    fila=1
    estado=0
    patron_identificador = r"[restaunRESTAUN]"
   
    current_cat=""
    current_id=""
    current_name=""
    current_precio=""
    current_descripcion=""   
    estado=0
    lexema=""
    columna=1

    for caracter in lineasMenu:
            columna +=1
            if caracter =="\n":
                fila+=1
                columna=0
                estado=0

            elif estado==0:
                lexema=""
                if caracter==" ":
                    continue
                elif caracter=="":
                    continue
                elif re.search(patron_identificador, caracter):
                        lexema += caracter
                        estado=1
                elif caracter=="\'":
                        lexema=caracter
                        numero_token +=1
                        tokens.append(Token(numero_token,lexema,fila,columna,"TK_comilla_simple"))
                        lexema=""
                        estado=6
                elif caracter=="[":
                        lexema=caracter        
                        numero_token+=1
                        tokens.append(Token(numero_token,lexema,fila,columna,"TK_corchete"))
                        lexema=""
                        estado=8
                else:
                    error=caracter
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,error,"Caracter no valido"))
                    estado=0
                    continue
            elif estado==1:
                if re.search(r"[a-zA-z\s]",caracter):
                    lexema+=caracter
                    continue
                elif caracter=="=":
                    if reservada =="":
                        if lexema.strip().lower()=="restaurante":
                            reservada=lexema.strip()
                            lexema=caracter
                            numero_token += 1
                            tokens.append(Token(numero_token,reservada,fila,columna-1,"Palabra Reservada"))
                        else:
                            numero_error+=1
                            errores.append(Error(numero_error,fila,columna-1,lexema.strip(),"Palabra reservada incorrecta"))
                            numero_token
                            tokens.append(Token(numero_token,lexema.strip(),fila,columna-1,"TK_cadena"))    
                    else:
                        numero_error +=1
                        errores.append(Error(numero_error,fila,columna-1,lexema.strip(),"Ya existe la palabra reservada"))
                        numero_token
                        tokens.append(Token(numero_token,lexema.strip(),fila,columna-1,"TK_cadena"))

                    
                    numero_token +=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"Tk_igual"))
                    lexema=""
                    estado=2
                else:
                    error=caracter
                    numero_error +=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido"))
                    break
            elif estado==2:
                if caracter==" ":
                    continue 
                elif caracter=="'":
                    lexema=caracter
                    numero_token+=1
                    tokens.append(Token(numero_token,lexema,fila,columna,"TK_comilla_simple"))
                    lexema=""
                    estado=3
                else:
                    error=caracter
                    numero_error +=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba ' "))
                    continue
            elif estado==3:
                if  re.search(r"[^']",caracter):    
                    lexema += caracter
                    continue   
                elif caracter=="'":
                    nombre=lexema.strip()
                    numero_token+=1
                    tokens.append(Token(numero_token,nombre,fila,columna-1,"TK_cadena"))
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"Tk_comilla_simple"))
                    lexema=""
                    estado=0
                else:
                    numero_error+=1
                    error=caracter
                    errores.append(Error(numero_error,fila,columna,error,"Se esperaba: ' ")) 
                    continue
            elif estado==6:
                if re.search(r"[A-Za-z\s]",caracter):
                    lexema +=caracter
                    continue
                elif caracter=="'":
                    current_cat=lexema.strip()
                    categorias.append(lexema.strip())
                    numero_token+=1
                    tokens.append(Token(numero_token,lexema.strip(),fila,columna-1,"TK_categoria"))
                    lexema=""
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                    estado=7
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido"))
            elif estado==7:
                if caracter==" ":
                    continue 
                elif caracter==":":
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_dos_puntos"))
                    estado=0
                    continue
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter invalido"))
            elif estado==8:
                if caracter==" ":
                    continue
                elif re.search(r"[a-z]",caracter):
                   lexema +=caracter
                   estado=9
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"El identificador debe iniciar en una letra minuscula"))
            elif estado==9:
                if caracter==" ":
                    continue
                elif re.search(r"[a-z0-9_]",caracter):
                    lexema+=caracter
                    continue
                elif caracter==";":
                    numero_token+=1
                    current_id=lexema.strip()
                    for element in identificadores:
                        if current_id==element:
                            numero_error+=1
                            errores.append(Error(numero_error,fila,columna,current_id,"Ya existe un producto con ese identificador"))
                        else:    
                            identificadores.append(current_id)
                    tokens.append(Token(numero_token,current_id,fila,columna-1,"TK_identificador"))

                    numero_token+=1 
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_punto_coma"))
                   
                    lexema=""
                    estado=10
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido en el identificador"))
                    continue

            elif estado==10:
                if caracter==" ":
                    continue
                elif caracter=="'":
                    numero_token+=1
                    tokens.append(Token(numero_token,lexema,fila,columna,"TK_comilla_simple"))
                    estado=11
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Se esperaba: ' "))
                    continue
            elif estado==11:
                if re.search(r"[^']",caracter):
                    lexema+=caracter
                    continue
                elif caracter=="'":
                    numero_token+=1
                    current_name=lexema.strip()
                    tokens.append(Token(numero_token,current_name,fila,columna-1,"TK_cadena"))
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                    lexema=""
                    estado=12
            elif estado==12:
                if caracter==" ":
                    continue
                elif caracter==";":
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_punto_coma"))
                    estado=13
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Se esperaba: ;"))
            elif estado==13:
                if caracter==" ":
                    continue
                elif re.search(r"[0-9]",caracter):
                    lexema +=caracter 
                    estado=14            
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Se esperaba un numero: 0-9"))
            elif estado==14:
                if re.search(r"[0-9]",caracter):
                    lexema +=caracter
                elif caracter==".":
                    lexema +=caracter
                    estado=15
                elif caracter==" ":
                    numero_token+=1
                    current_precio="{0:.2f}".format(float(lexema))
                    tokens.append(Token(numero_token,current_precio,fila,columna-1,"TK_numero"))
                    lexema=""
                    estado=16
                    continue
                elif caracter==r";":
                    numero_token+=1
                    current_precio="{0:.2f}".format(float(lexema))
                    tokens.append(Token(numero_token,current_precio,fila,columna-1,"TK_numero"))
                    lexema=""
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_punto_coma"))
                    estado=17
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido"))
            elif estado==15:
                if re.search(r"[0-9]",caracter):
                    lexema+=caracter
                    continue
                elif caracter==" ":
                    numero_token+=1
                    current_precio="{0:.2f}".format(float(lexema))
                    tokens.append(Token(numero_token,current_precio,fila,columna-1,"TK_numero"))
                    lexema=""
                    estado=16 
                    continue
                elif caracter==r";":
                    numero_token+=1
                    current_precio="{0:.2f}".format(float(lexema))
                    tokens.append(Token(numero_token,current_precio,fila,columna-1,"TK_numero"))
                    lexema=""
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_punto_coma"))
                    estado=17
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba un valor [0-9]"))                
            elif estado==16:
                if caracter==" ":
                    continue
                elif caracter==";":
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_punto_coma"))
                    estado=17
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba: ;"))
            elif estado ==17:
                if caracter==" ":
                    continue
                elif caracter=="'":
                    
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                    estado=18
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Caracter no valido, se esperaba: '"))
            elif estado==18:
                if re.search(r"[^']",caracter):
                    lexema+=caracter
                    continue
                elif caracter=="'":
                    numero_token+=1
                    current_descripcion=lexema.strip()
                    tokens.append(Token(numero_token,current_descripcion,fila,columna,"TK_cadena"))
                    lexema=""
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_comilla_simple"))
                    platillos.append(Platillo(current_cat,current_id,current_name,current_precio,current_descripcion))
                    estado=19
                else:
                    numero_error+=1
                    errores.append(Error(numero_error,fila,columna,caracter,"Se esperaba: '"))
                    continue
            elif estado==19:
                if caracter==" ":
                    continue
                elif caracter=="]":
                    numero_token+=1
                    tokens.append(Token(numero_token,caracter,fila,columna,"TK_corchete"))
                    estado=0
                    continue

    if errores==[]:
        menu=Menu(nombre,categorias,platillos)
        generarMenuHTML(menu)
        generarTokensHTML(tokens)
    else:
        generarErroresHTML(errores)  
        generarTokensHTML(tokens)  

def generarMenuHTML(menu):
    inicio="<!doctype html><html><head> <title>Menu</title> </head><body style=\"background-image: url(https://www.wallpapertip.com/wmimgs/50-503868_462280-title-man-made-bar-wallpaper-fancy-restaurant.jpg)\"><h1 style=\"text-align: center;\"><span style=\"font-size:48px;\"><span style=\"color:#ffffff; background-color: rgba(0, 0, 0, 0.5);\">"+str(menu.restaurante)+"</span></span></h1><hr /><div style=\"background-color: rgba(255, 255, 255, 0.8);margin-left: 500px; margin-right: 500px;padding-top: 20px; padding-bottom: 50px;border-radius: 8px;\">"
    mitad=""
    for element in menu.categorias:
        mitad=mitad+"<p style=\"margin-left: 120px;\"><strong><span style=\"font-size:28px;\">"+str(element)+":</span></strong></p>"
        for subelement in menu.platillos:
            if str(subelement.categoria)==str(element):
                mitad=mitad+"<p style=\"margin-left: 160px;\">"+str(subelement.nombre)+"&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Q "+str(subelement.precio)+"<br />"+str(subelement.descripcion)+"</p>"
    fin="</div></body> </html>"
    cadena=inicio+mitad+fin
    archivo=open('Menu.html','w',encoding="utf-8")
    archivo.write(cadena)
    archivo.close()
    os.system('Menu.html')
    print("Menu generado con exito")

def generarTokensHTML(tokens):
    inicio="<!doctype html><html><head> <title>Tokens Menu</title> </head><body><h1 style=\"text-align: center; color: #3f7320;\">Tokens:</h1> <table border=\"1\" align=\"center\" style=\"background-color:#ffffcc;border-collapse:collapse;border:1px solid #ffcc00\"><thead><tr><td><span style=\"color: #c82828;\">No.</span></td><td><span style=\"color: #c82828;\">Lexema</span></td><td><span style=\"color: #c82828;\">Fila</span></td><td><span style=\"color: #c82828;\">Columna</span></td><td><span style=\"color: #c82828;\">Token</span></td></tr></thead><tbody>"
    mitad=""
    for element in tokens:
        mitad=mitad+"<tr><td>"+str(element.numero)+"</td><td>"+str(element.lexema)+"</td><td>"+str(element.fila)+"</td><td>"+str(element.columna)+"</td><td>"+str(element.descripcion)+"</td></tr>"
    fin="</tbody></table>"
    cadena=inicio+mitad+fin
    archivo=open('Tokens.html','w',encoding="utf-8")
    archivo.write(cadena)
    archivo.close()
    os.system('Tokens.html')
    print("Tabla de Tokens generada con exito")


def generarErroresHTML(errores):
    inicio="<!doctype html><html><head> <title>Errores Menu</title> </head><body><h1 style=\"text-align: center; color: #3f7320;\">Errores:</h1> <table border=\"1\" align=\"center\" style=\"background-color:#ffffcc;border-collapse:collapse;border:1px solid #ffcc00\"><thead><tr><td><span style=\"color: #c82828;\">No.</span></td><td><span style=\"color: #c82828;\">Fila</span></td><td><span style=\"color: #c82828;\">Columna</span></td><td><span style=\"color: #c82828;\">Caracter</span></td><td><span style=\"color: #c82828;\">Descripción</span></td></tr></thead><tbody>"
    mitad=""
    for element in errores:
        mitad=mitad+"<tr><td>"+str(element.numero)+"</td><td>"+str(element.fila)+"</td><td>"+str(element.columna)+"</td><td>"+str(element.caracter)+"</td><td>"+str(element.descripcion)+"</td></tr>"
    fin="</tbody></table>"
    cadena=inicio+mitad+fin
    archivo=open('Errores.html','w',encoding="utf-8")
    archivo.write(cadena)
    archivo.close()
    os.system('Errores.html')
    print("Tabla de Errores generada con exito")


def limpiar():
    global lineasMenu,errores,tokens,platillos,reservada,nombre,categorias,menu,identificadores
    lineasMenu=""
    errores.clear()
    tokens.clear()
    platillos.clear()
    reservada=""
    nombre=""
    categorias.clear()
    menu=None
    identificadores.clear()

def generarArbol():
    global menu
    
    if menu is not None:
        inicio= 'digraph G {titulo[label="'+menu.restaurante+'"]\n'
        mitad=""
        id_cat=0
        for element in menu.categorias:
            id_cat+=1
            id_prod=0
            mitad=mitad+'categoria'+str(id_cat)+'[label="'+element+'"]\ntitulo -> categoria'+str(id_cat)+"\n"
            for subelement in menu.platillos:
                id_prod+=1
                if subelement.categoria==element:
                    mitad=mitad+'prod'+str(id_prod)+'[label="'+str(subelement.nombre)+'      Q'+str(subelement.precio)+"\n"+subelement.descripcion+'"]\ncategoria'+str(id_cat)+' ->'+'prod'+str(id_prod)+"\n"
        fin="}"
        temp=inicio+mitad+fin
        s = Source(temp, filename="arbol", format="pdf") 
        s.view()
    else:
        print("Primero debe generar un menu de manera correcta para crear el arbol.")