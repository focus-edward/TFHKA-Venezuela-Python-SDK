"""
EJEMPLO DE INTEGRACIÓN PARA GENERAR NOTA DE DÉBITO SIMPLE CON IGTF - (PYTHON 3)

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
     DEFINIR LA INFORMACIÓN QUE VA UTILIZAR PARA GENERAR NOTA DE DÉBITO SIMPLE CON IGTF

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
     UTILIZAR LOS MÉTODOS Y ATRIBUTOS QUE EL OFRECE LA LIBRERIA PARA GENERAR NOTA DE DÉBITO SIMPLE CON IGTF.

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

class NotaDebitoSimpleIGTF():

    # PASO 2: Definir la información que va a utilizar en la nota de débito.
    INVOICE_NUMBER_AFFECTED = "iF*01020000001"                  # Información del Número de Factura Afectada
    INVOICE_DATE_AFFECTED = "iD*23/06/2022"                     # Información de la Fecha de la Factura Afectada
    REGISTRY_NUMBER = "iI*Z1F1234567"                           # Información del Número de Registro

    RIF = "iR*J-312171197"                                      # Información del Registro de Identficación Fiscal
    SOCIAL_REASON = "iS*THE FACTORY HKA, C.A."                  # Información de Razón Social
    ADDRESS_LINE1 = "i00DIRECCION: LA CALIFORNIA"               # Información de Dirección linea 1
    ADDRESS_LINE2 = "i01CARACAS"                                # Información de Dirección linea 2

    PLU1 = "`0000000001000001000Producto 1"                     # Información  de PLU: Tasa Exento  , cantidad 1, monto 0.10 bs, nombre del PLU
    PLU2 = "`1000000001000001000Producto 2"                     # Información  de PLU: Tasa General , cantidad 1, monto 0.10 bs, nombre del PLU
    PLU3 = "`2000000001000001000Producto 3"                     # Información  de PLU: Tasa Reducida, cantidad 1, monto 0.10 bs, nombre del PLU
    PLU4 = "`3000000001000001000Producto 4"                     # Información  de PLU: Tasa Ampliada, cantidad 1, monto 0.10 bs, nombre del PLU

    COMMAND_SUBTOTAL = "3"                                      # Comando de subtotal de nota de débito
    COMMAND_FLAG50 = "PJ5001"                                   # Comando para establecer el Flag 50 en 01
    COMMAND_PAGOTOTAL = "121"                                   # Comando de Totalizar nota de débito
    COMMAND_CLOSE = "199"                                       # Comando de Cierre nota de débito
    COMMAND_COMMENT = "BEJEMPLO DE NOTA DE DEBITO CON IGTF"     # Comando envio para Introducir un comentario

    #PASO 3: Instanciar la libreria y definir los parametros por defecto que utilizaremos
    Printer = TfhkaPyGD.Tfhka()
    PORT = "COM3"                                               # Definimos el puerto serial donde esta conectada la impresora fiscal
    PortOpen = False
    Respuesta = False

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
            print("")


            Respuesta = Printer.SendCmd(COMMAND_FLAG50)
            if not Respuesta: print("!!! Comando No Aceptado: " + COMMAND_FLAG50)
            else: print("*** Comando Enviado: " + COMMAND_FLAG50)
            
            Respuesta = Printer.SendCmd(INVOICE_NUMBER_AFFECTED)
            if not Respuesta: print("Comando No Aceptado: " + INVOICE_NUMBER_AFFECTED)
            else: print("*** Comando Enviado: " + INVOICE_NUMBER_AFFECTED)

            Respuesta = Printer.SendCmd(INVOICE_DATE_AFFECTED)
            if not Respuesta: print("Comando No Aceptado: " + INVOICE_DATE_AFFECTED)
            else: print("*** Comando Enviado: " + INVOICE_DATE_AFFECTED)

            Respuesta = Printer.SendCmd(REGISTRY_NUMBER)
            if not Respuesta: print("Comando No Aceptado: " + REGISTRY_NUMBER)
            else: print("*** Comando Enviado: " + REGISTRY_NUMBER)

            Respuesta = Printer.SendCmd(SOCIAL_REASON)
            if not Respuesta: print("Comando No Aceptado: " + SOCIAL_REASON)
            else: print("*** Comando Enviado: " + SOCIAL_REASON)

            Respuesta = Printer.SendCmd(RIF)
            if not Respuesta: print("Comando No Aceptado: " + RIF)
            else: print("*** Comando Enviado: " + RIF)

            Respuesta = Printer.SendCmd(ADDRESS_LINE1)
            if not Respuesta: print("Comando No Aceptado: " + ADDRESS_LINE1)
            else: print("*** Comando Enviado: " + ADDRESS_LINE1)

            Respuesta = Printer.SendCmd(ADDRESS_LINE2)
            if not Respuesta: print("Comando No Aceptado: " + ADDRESS_LINE2)
            else: print("*** Comando Enviado: " + ADDRESS_LINE2)

            Respuesta = Printer.SendCmd(COMMAND_COMMENT)
            if not Respuesta: print("Comando No Aceptado: " + COMMAND_COMMENT)
            else: print("*** Comando Enviado: " + COMMAND_COMMENT)

            Respuesta = Printer.SendCmd(PLU1)
            if not Respuesta: print("Comando No Aceptado: " + PLU1)
            else: print("*** Comando Enviado: " + PLU1)

            Respuesta = Printer.SendCmd(PLU2)
            if not Respuesta: print("Comando No Aceptado: " + PLU2)
            else: print("*** Comando Enviado: " + PLU2)

            Respuesta = Printer.SendCmd(PLU3)
            if not Respuesta: print("Comando No Aceptado: " + PLU3)
            else: print("*** Comando Enviado: " + PLU3)

            Respuesta = Printer.SendCmd(PLU4)
            if not Respuesta: print("Comando No Aceptado: " + PLU4)
            else: print("*** Comando Enviado: " + PLU4)

            Respuesta = Printer.SendCmd(COMMAND_COMMENT)
            if not Respuesta: print("Comando No Aceptado: " + COMMAND_COMMENT)
            else: print("*** Comando Enviado: " + COMMAND_COMMENT)

            Respuesta = Printer.SendCmd(COMMAND_SUBTOTAL)
            if not Respuesta: print("Comando No Aceptado: " + COMMAND_SUBTOTAL)
            else: print("*** Comando Enviado: " + COMMAND_SUBTOTAL)

            Respuesta = Printer.SendCmd(COMMAND_PAGOTOTAL)
            if not Respuesta: print("Comando No Aceptado: " + COMMAND_PAGOTOTAL)
            else: print("*** Comando Enviado: " + COMMAND_PAGOTOTAL)

            Respuesta = Printer.SendCmd(COMMAND_CLOSE)
            if not Respuesta: print("Comando No Aceptado: " + COMMAND_CLOSE)
            else: print("*** Comando Enviado: " + COMMAND_CLOSE)
            
            # Cerrar Puerto
            Printer.CloseFpctrl() # En el caso de los software administrativos es recomendable que se cierre el puerto solo cuando la impresora no opere mas en el dia
            
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