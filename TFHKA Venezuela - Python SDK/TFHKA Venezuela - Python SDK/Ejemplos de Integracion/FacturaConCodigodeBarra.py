"""
EJEMPLO DE INTEGRACIÓN PARA GENERAR FACTURA CON CODIGO DE BARRAS - (PYTHON 3)

OBJETIVO: Ejemplificar el proceso de conexión, acceso y uso de las propiedades y métodos ofrecidos por la
          libreria TfhkaPy a través del lenguaje de programación PYTHON
____________________________________________________________________________________________________________________________
FORMA DE TRABAJO SUGERIDA
......................................................................................................................... 
* PASO 1
.........................................................................................................................  
     IMPORTAR LA LIBRERIA TfhkaPy
        
       * EXPLICACIÓN:
        
         1.- Consiste en importar la libreria "TfhkaPy"
......................................................................................................................... 
* PASO 2
.........................................................................................................................
     DEFINIR LA INFORMACIÓN QUE VA UTILIZAR PARA GENERAR FACTURA CON CODIGO DE BARRAS

       * EXPLICACIÓN:
 
         1.- En su código fuente defina un par de constantes donde almacenar y asígneles
             la información correspondiente.
         2.- Cualquier información adicional consulte el MANUAL DE PROTOCOLOS Y COMANDOS. El cual debe
             solicitar departamento de integracion y soporte.

......................................................................................................................... 
* PASO 3
.........................................................................................................................
     INSTANCIAR EL OBJETO "Tfhka" DE LA LIBRERIA TfhkaPy, A TRAVÉS DE LA IMPORTACIÓN CREADA EN EL PASO 1

       * EXPLICACIÓN:
 
         1.- En su código fuente cree un objeto de tipo "TfhkaPy".
         2.- Defina los atributos que desea configurar por defecto.

......................................................................................................................... 
* PASO 4
.........................................................................................................................
     UTILIZAR LOS MÉTODOS Y ATRIBUTOS QUE EL OFRECE LA LIBRERIA PARA GENERAR FACTURA CON CODIGO DE BARRAS

#      * EXPLICACIÓN:
#
#          - En su código fuente defina las Clases, variables, funciones y objetos que se requieran para utilizar
#            directamente los métodos y atributos que la libreria Tfhka pone a su disposición.
#            Dichos objetos pueden ser accedidos a través de la importacion de las librerias expuestas en el Paso 1
#
#             Estructura de funciones:
#   
#               def <Nombre de la funcion> ([parametro 1], [parametro 2],...)             
#
#
#               Nombre de la función:   Identificador o nombre que se le da a la función.
#
#               parámetro:             Datos de entrada con los que trabajará la función, puede no llevar.
#
#              Actualmente, la libreria Tfhka ofrece los métodos que se describen y detallan a continuación:

             * Método OpenFpCtrl():
               --------------------------------------------------------------------------------------------------------     
               Permite realizar la apertura del puerto de comunicaciones por el cual se establecerá comunicación
               con la impresora. Este método se ejecuta en el constructor único de la clase, pero puede ser 
               ejecutado nuevamente de ser requerido, tal y como se muestra a continuación:
                                           
               OpenFpctrl(String IpPortName)

               --------------------------------------------------------------------------------------------------------

             * Método CloseFpCtrl():
               --------------------------------------------------------------------------------------------------------     
               Permite cerrar del puerto COM asociado, abierto anteriormente, pero puede ser 
               ejecutado nuevamente de ser requerido, tal y como se muestra a continuación:
                                           
               CloseFpctrl()

               --------------------------------------------------------------------------------------------------------

             * Método SendCmd():
               --------------------------------------------------------------------------------------------------------
               Permite realizar el envío de comandos hacia la impresora, en forma de tramas de caracteres
               ASCII, tal como es descrito en los manuales de integración de las respectivas impresoras, y en
               el manual general de protocolos y comandos del protocolo TFHKA, tal y como se muestra a continuación:
                                           
               SendCmd(String Cmd)

               --------------------------------------------------------------------------------------------------------


"""
###################################  EJEMPLO DE PROGRAMA PYTHON USA LA LIBRERIA TfhkaPy ###################################

    #A continuación se presenta el código de ejemplo de una aplicación PYTHON de cónsola que utiliza directamente los objetos
    #                               (Clases, atributos y métodos) que ofrece la libreria.

############################################################################################################################

# PASO 1: Consiste en importar la libreria
from Libreria import TfhkaPyGD

class CodigosDeBarras():

    # PASO 2: Definir la información que va a utilizar en la factura.
    COMMAND_FLAG30_00 = "PJ3000"                            #Comando para que NO muestre código numérico asociado al código de barra se muestre debajo de éste
    COMMAND_FLAG30_01 = "PJ3001"                            #Comando para que muestre código numérico asociado al código de barra se muestre debajo de éste

    COMMAND_FLAG43_00 = "PJ4300"                            #Comando código de EAN 13: 12 Caracteres Numéricos fijos
    COMMAND_FLAG43_01 = "PJ4301"                            #Comando código de ITF: 1 a 32 Caracteres Numéricos (la cantidad de caracteres debe ser un número par)
    COMMAND_FLAG43_02 = "PJ4302"                            #Comando código de CODE128: 1 a 32 Caracteres Alfanuméricos
    COMMAND_FLAG43_03 = "PJ4303"                            #Comando código de CODE39: 32 caracteres alfanuméricos
    COMMAND_FLAG43_04 = "PJ4304"                            #Comando código de QR: 120 caracteres alfanuméricos
    COMMAND_FLAG43_05 = "PJ4305"                            #Comando código de PDF417: 120 caracteres alfanuméricos

    RIF = "iR*J-312171197"                                  #Información del Registro de Identficación Fiscal
    SOCIAL_REASON = "iS*THE FACTORY HKA, C.A."              #Información de Razón Social
    ADDRESS_LINE1 = "i00DIRECCION: LA CALIFORNIA"           #Información de Dirección linea 1
    ADDRESS_LINE2 = "i01CARACAS"                            #Información de Dirección linea 2


    CODE_EAN = "012345678912"                               #codigo de barras EAN 13
    CODE_ITF = "0123456789012345"                           #codigo de barras ITF
    CODE_CODE128 = "0123456789ABCDF"                        #codigo de barras CODE128
    CODE_CODE39 = "0123456789ABCDEFGHJ0"         #codigo de barras CODE39
    CODE_PDF417 = "0123456789ABCDEFGHJ01234567890123456789ABCDEFGHJ01234567890123456789ABCDEFGHJ01234567890123456789ABCDEFGHJ0123456789" #codigo de barras PDF417
    CODE_QR = "0123456789ABCDEFGHJ01234567890123456789ABCDEFGHJ01234567890123456789ABCDEFGHJ01234567890123456789ABCDEFGHJ0123456789"     #codigo de barras QR

    COMMAND_CB_IN = "Y"                                     #comando para establecer Código de Barra impreso dentro de la factura
    COMMAND_CB_DONW = "y"                                   #Código de Barra impreso en el pie de página de la factura
    
    PLU1 = " 000000001000001000Producto 1";                 #Información  de PLU: Tasa Exento  , cantidad 1, monto 0.10 bs, nombre del PLU
    PLU2 = "!000000001000001000Producto 2";                 #Información  de PLU: Tasa General , cantidad 1, monto 0.10 bs, nombre del PLU
    
    COMMAND_FLAG50 = "PJ5000";                              #Comando para establecer el Flag 50 en 00
    COMMAND_PAGOTOTAL = "101";                              #comando de Totalizar  Factura
    COMMAND_COMMENT = "@EJEMPLO DE CODIGO de BARRAS";       #Comando envio para Introducir un comentario
    CODE_ENVIO = "";                                        #Codigo a enviar

    #PASO 3: Instanciar la libreria y definir los parametros por defecto que utilizaremos
    Printer = TfhkaPyGD.Tfhka()
    PORT = "COM3"                                           # Definimos el puerto serial donde esta conectada la impresora fiscal
    PortOpen = False
    Respuesta = False
    pant = " "

    try:
        #PASO 4: Utilizar los Métodos y atributos que ofrece la libreria TfhkaPy y manejar la respuesta.
        PortOpen = Printer.OpenFpctrl(PORT)
        CTS_STATUS = Printer._HandleCTSRTS()
        
        if PortOpen:
            
            print("Puerto: "+ PORT + " ABIERTO")
            print("")
            print("###############")
            print("")
            input("Presione enter para continuar ...")


            Respuesta = Printer.SendCmd(COMMAND_FLAG50)
            if not Respuesta: print("!!! Comando No Aceptado: " + COMMAND_FLAG50)
            else: print("*** Comando Enviado: " + COMMAND_FLAG50)

            print("")
            print("###############")
            print("")
            
            print("Desea que el código numérico asociado al código de barra se muestre debajo de éste:")
            print("a - Si")
            print("b - NO")
            print("Elija su opcion: ")
            pant = input()

            while pant != "a" and pant != "A" and pant != "b" and pant != "B":
              pant=input("Por favor elegir entre a o b\n")
              print("")
        
            if pant == "a" or "A":
              BResp = Printer.SendCmd(COMMAND_FLAG30_01)
              if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_FLAG30_01)
              else: print("*** Comando Enviado: " + COMMAND_FLAG30_01)

            elif pant == "b" or "B":
              BResp = Printer.SendCmd(COMMAND_FLAG30_00)
              if not BResp: print("!!! Comando No Aceptado: " + COMMAND_FLAG30_00)
              else: print("*** Comando Enviado: " + COMMAND_FLAG30_00)
            
            else:
              print("Comando no habilitado")
                
            print("")
            print("###############")
            print("")
            
            print("Seleccione el tipo de codigo de barras:")
            print("a - EAN 13")
            print("b - ITF")
            print("c - CODE128")
            print("d - CODE39")
            print("e - PDF417")
            print("f - QR")
            print("Elija su opcion: ")
            pant = input()    

            if pant == "a" or pant == "A":
              CODE_ENVIO = CODE_EAN
              BResp = Printer.SendCmd(COMMAND_FLAG43_00)
              if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_FLAG43_00)
              else: print("*** Comando Enviado: " + COMMAND_FLAG43_00)

            elif pant == "b" or pant == "B":
              CODE_ENVIO = CODE_ITF
              BResp = Printer.SendCmd(COMMAND_FLAG43_01)
              if not BResp: print("!!! Comando No Aceptado: " + COMMAND_FLAG43_01)
              else: print("*** Comando Enviado: " + COMMAND_FLAG43_01)
            
            elif pant == "c" or pant == "C":
              CODE_ENVIO = CODE_CODE128
              BResp = Printer.SendCmd(COMMAND_FLAG43_02)
              if not BResp: print("!!! Comando No Aceptado: " + COMMAND_FLAG43_02)
              else: print("*** Comando Enviado: " + COMMAND_FLAG43_02)
            
            elif pant == "d" or pant == "D":
              CODE_ENVIO = CODE_CODE39
              BResp = Printer.SendCmd(COMMAND_FLAG43_03)
              if not BResp: print("!!! Comando No Aceptado: " + COMMAND_FLAG43_03)
              else: print("*** Comando Enviado: " + COMMAND_FLAG43_03)
            
            elif pant == "e" or pant == "E":
              CODE_ENVIO = CODE_PDF417
              BResp = Printer.SendCmd(COMMAND_FLAG43_05)
              if not BResp: print("!!! Comando No Aceptado: " + COMMAND_FLAG43_05)
              else: print("*** Comando Enviado: " + COMMAND_FLAG43_05)
            
            elif pant == "f" or pant == "F":
              CODE_ENVIO = CODE_QR
              BResp = Printer.SendCmd(COMMAND_FLAG43_04)
              if not BResp: print("!!! Comando No Aceptado: " + COMMAND_FLAG43_04)
              else: print("*** Comando Enviado: " + COMMAND_FLAG43_04)
            
            else:
              print("Comando no habilitado")

            print("")
            print("###############")
            print("")

            BResp = Printer.SendCmd(SOCIAL_REASON)
            if not BResp: print("Comando No Aceptado: " + SOCIAL_REASON)
            else: print("*** Comando Enviado: " + SOCIAL_REASON)

            BResp = Printer.SendCmd(RIF)
            if not BResp: print("Comando No Aceptado: " + RIF)
            else:  print("*** Comando Enviado: " + RIF)

            BResp = Printer.SendCmd(ADDRESS_LINE1)
            if not BResp: print("Comando No Aceptado: " + ADDRESS_LINE1)
            else: print("*** Comando Enviado: " + ADDRESS_LINE1)

            BResp = Printer.SendCmd(ADDRESS_LINE2)
            if not BResp: print("Comando No Aceptado: " + ADDRESS_LINE2)
            else: print("*** Comando Enviado: " + ADDRESS_LINE2)

            BResp = Printer.SendCmd(COMMAND_COMMENT)
            if not BResp: print("Comando No Aceptado: " + COMMAND_COMMENT)
            else: print("*** Comando Enviado: " + COMMAND_COMMENT)
            
            BResp = Printer.SendCmd(COMMAND_CB_IN + CODE_ENVIO)
            if not BResp: print("Comando No Aceptado: " + COMMAND_CB_IN + CODE_ENVIO)
            else: print("*** Comando Enviado: " + COMMAND_CB_IN + CODE_ENVIO)

            BResp = Printer.SendCmd(PLU1)
            if not BResp: print("Comando No Aceptado: " + PLU1)
            else: print("*** Comando Enviado: " + PLU1)
            
            BResp = Printer.SendCmd(COMMAND_CB_IN + CODE_ENVIO)
            if not BResp: print("Comando No Aceptado: " + COMMAND_CB_IN + CODE_ENVIO)
            else: print("*** Comando Enviado: " + COMMAND_CB_IN + CODE_ENVIO)

            BResp = Printer.SendCmd(PLU2)
            if not BResp: print("Comando No Aceptado: " + PLU2)
            else: print("*** Comando Enviado: " + PLU2)

            BResp = Printer.SendCmd(COMMAND_COMMENT)
            if not BResp: print("Comando No Aceptado: " + COMMAND_COMMENT)
            else: print("*** Comando Enviado: " + COMMAND_COMMENT)

            print("")
            print("###############")
            print("")

            print("Desea imprimir el codigo de barras en el pie de pagina:")
            print("a - Si")
            print("b - NO")

            print("Elija su opcion: ")
            pantb = input()

            if pantb == "a" or pantb == "A":

              if pant == "a" or pant == "A":
                CODE_ENVIO = CODE_EAN
                BResp = Printer.SendCmd(COMMAND_CB_DONW + CODE_ENVIO)
                if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_CB_DONW + CODE_ENVIO)
                else: print("*** Comando Enviado: " + COMMAND_CB_DONW + CODE_ENVIO)              

              elif pant == "b" or pant == "B":
                CODE_ENVIO = CODE_ITF
                BResp = Printer.SendCmd(COMMAND_CB_DONW + CODE_ENVIO)
                if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_CB_DONW + CODE_ENVIO)
                else: print("*** Comando Enviado: " + COMMAND_CB_DONW + CODE_ENVIO)    

              elif pant == "c" or pant == "C":
                CODE_ENVIO = CODE_CODE128
                BResp = Printer.SendCmd(COMMAND_CB_DONW + CODE_ENVIO)
                if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_CB_DONW + CODE_ENVIO)
                else: print("*** Comando Enviado: " + COMMAND_CB_DONW + CODE_ENVIO)    

              elif pant == "d" or pant == "D":
                CODE_ENVIO = CODE_CODE39
                BResp = Printer.SendCmd(COMMAND_CB_DONW + CODE_ENVIO)
                if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_CB_DONW + CODE_ENVIO)
                else: print("*** Comando Enviado: " + COMMAND_CB_DONW + CODE_ENVIO)

              elif pant == "e" or pant == "E":
                CODE_ENVIO = CODE_PDF417
                BResp = Printer.SendCmd(COMMAND_CB_DONW + CODE_ENVIO)
                if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_CB_DONW + CODE_ENVIO)
                else: print("*** Comando Enviado: " + COMMAND_CB_DONW + CODE_ENVIO)       

              elif pant == "f" or pant == "F":
                CODE_ENVIO = CODE_QR
                BResp = Printer.SendCmd(COMMAND_CB_DONW + CODE_ENVIO)
                if (not BResp): print("!!! Comando No Aceptado: " + COMMAND_CB_DONW + CODE_ENVIO)
                else: print("*** Comando Enviado: " + COMMAND_CB_DONW + CODE_ENVIO)                                 
            
            else:
              print("Comando no habilitado")

            print("")
            print("###############")
            print("")

            BResp = Printer.SendCmd(COMMAND_PAGOTOTAL)
            if not BResp: print("Comando No Aceptado: " + COMMAND_PAGOTOTAL)
            else: print("*** Comando Enviado: " + COMMAND_PAGOTOTAL)

            # Cerrar Puerto
            Printer.CloseFpctrl()  # En el caso de los software administrativos es recomendable que se cierre el puerto solo cuando la impresora no opere mas en el dia
            
            print("")
            print("###############")
            print("")
            #input("Presione enter para Salir ...")
                            
            
        else:
            print("")
            print("###############")
            print("")            
            print("NO SE PUDO ESTABLECER COMUNICACION CON LA IMPRESORA")
            print("PUERTO: " + PORT + " CERRADO")
            print("")
            print("###############")
            print("")
   
    except Exception as ex: 
      print("OCURRIO UNA EXCEPCION: \nDetalles del Error: \n ")
      print("Error al abrir el puerto serial:", ex)
      print(type(ex).__name__)