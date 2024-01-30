"""
EJEMPLO DE INTEGRACIÓN PARA ENVIAR ARCHIVO DE FACTURA - (PYTHON 3)

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
     DEFINIR LA INFORMACIÓN QUE VA UTILIZAR PARA ENVIAR ARCHIVO DE FACTURA

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

class ArchivoFactura():

    # PASO 2: Definir la información que va a utilizar en la factura.
    FACT = "Archivos de Factura Txt/FACT.txt"                                  # Ruta Archivo de factura
    FACT_PP = "Archivos de Factura Txt/FACT_PP.txt"                            # Ruta Archivo de factura pago parcial

    FACT_IGTF = "Archivos de Factura Txt/FACT_IGTF.txt"                        # Ruta Archivo de factura IGTF
    FACT_IGTF_PP = "Archivos de Factura Txt/FACT_IGTF_PP.txt"                  # Ruta Archivo de factura IGTF pago parcial
    FACT_COD_BARRAS = "Archivos de Factura Txt/FACT_COD_BARRAS.txt"
    DOC_NOFISCAL = "Archivos de Factura Txt/DOCUMENTO_NOFISCAL.txt"

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


            print("Seleccione el tipo de Factura:")
            print("a - Factura Simple")
            print("b - Factura Simple con pago parcial")
            print("c - Factura Simple IGTF")
            print("d - Factura Simple IGTF con pago parcial")
            print("f - Factura Simple con Codigo de Barras")
            print("g - Documento no fiscal")
            print("Elija su opcion: ")
            pant = input()
            
            if pant == "a" or pant == "A": 
                BResp = Printer.SendCmdFile(FACT)
                if BResp: print("!!! Comando No Aceptado: " + FACT)
                else: print("*** Comando Enviado: " + FACT)
            
            elif pant == "b" or pant == "B": 
                BResp = Printer.SendCmdFile(FACT_PP)
                if BResp: print("!!! Comando No Aceptado: " + FACT_PP)
                else: print("*** Comando Enviado: " + FACT_PP)
            
            elif pant == "c" or pant == "C": 
                BResp = Printer.SendCmdFile(FACT_IGTF)
                if BResp: print("!!! Comando No Aceptado: " + FACT_IGTF)
                else: print("*** Comando Enviado: " + FACT_IGTF)
            
            elif pant == "d" or pant == "D": 
                BResp = Printer.SendCmdFile(FACT_IGTF_PP)
                if BResp: print("!!! Comando No Aceptado: " + FACT_IGTF_PP)
                else: print("*** Comando Enviado: " + FACT_IGTF_PP)

            elif pant == "f" or pant == "F": 
                BResp = Printer.SendCmdFile(FACT_COD_BARRAS)
                if BResp: print("!!! Comando No Aceptado: " + FACT_COD_BARRAS)
                else: print("*** Comando Enviado: " + FACT_COD_BARRAS)

            elif pant == "g" or pant == "G": 
                BResp = Printer.SendCmdFile(DOC_NOFISCAL)
                if BResp: print("!!! Comando No Aceptado: " + DOC_NOFISCAL)
                else: print("*** Comando Enviado: " + DOC_NOFISCAL)

            else: print("Comando no habilitado")


    # Cerrar Puerto
            Printer.CloseFpctrl()
            
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