"""
EJEMPLO DE INTEGRACIÓN PARA OBTENER INFORMACION DE IMPRESORA FISCAL - (PYTHON 3)

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
     DEFINIR LA INFORMACIÓN QUE VA UTILIZAR PARA OBTENER INFORMACION DE IMPRESORA FISCAL

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
     UTILIZAR LOS MÉTODOS Y ATRIBUTOS QUE EL OFRECE LA LIBRERIA PARA OBTENER INFORMACION DE IMPRESORA FISCAL.

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
class InformacionImpresoraFiscal():

    Printer = TfhkaPyGD.Tfhka()
    
    
    PORT = "COM3"                                           # Definimos el puerto serial donde esta conectada la impresora fiscal
    PortOpen = False
    Respuesta = False
    pant = " "
    # PASO 2: Definir la información que va a utilizar en la factura.
   

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

            status = Printer.ReadFpStatus()
            print("INFORMACIÓN DE ESTATUS Y ERROR DE LA IMPRESORA FISCAL")
            print(status)

            print("")
            print("###############")
            print("")

            InfoPrinter = Printer.GetSVPrinterData()
            print("MODELO DE IMPRESORA FISCAL")
            print("")
            print("Modelo de Impresora: " + InfoPrinter.Pmodel())

            print("")
            print("###############")
            print("")

            StatusS1 = Printer.GetS1PrinterData()
            print("INFORMACIÓN DE ESTATUS S1 DE LA IMPRESORA FISCAL")
            print("")
            print("Número de Registro impresora fiscal: " + StatusS1.RegisteredMachineNumber())
            print("RIF registrado de la maquina: " + StatusS1.Rif())
            print("Cant. de Facturas Emitidas en el día: " , StatusS1.QuantityOfInvoicesToday())
            print("Cantidad de Documentos No Fiscales: " , StatusS1.QuantityNonFiscalDocuments())
            print("Contador de Reportes Diarios (Z): " , StatusS1.DailyClosureCounter())


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