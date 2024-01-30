"""
EJEMPLO DE INTEGRACIÓN PARA GENERAR DOCUMENTO NO FISCAL - (PYTHON 3)

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
     DEFINIR LA INFORMACIÓN QUE VA UTILIZAR PARA GENERAR DOCUMENTO NO FISCAL

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
     UTILIZAR LOS MÉTODOS Y ATRIBUTOS QUE EL OFRECE LA LIBRERIA PARA GENERAR DOCUMENTO NO FISCAL.

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

class DocumentoNoFiscal():

    # PASO 2: Definir la información que va a utilizar en la documento no fiscal.
    FLAG_3001 = "PJ3001"                                                            #Activa Flag para Codigo de Barras
    FLAG_4303 = "PJ4303"                                                            #Activa el tipo de codigo de Barras CODE39

    LINE1 = "80" + "0" + "Documento de prueba para ejemplificar el uso "            #Comentario con texto normal
    LINE2 = "80" + "*" + "de los Documentos NO Fiscales y de sus"                   #Comentario con texto negrita
    LINE3 = "80" + ">" + "distintas caracteristicas y efectos....."                 #Comentario con texto expandido
    LINE4 = "80" + "$" + "dichos documentos pueden ser utilizados para"             #Comentario con texto negrita + centrado + doble ancho
    LINE5 = "80" + "!" + "la impresion de reportes internos de los Sistemas Adm."   #Comentario con texto centrado
    LINE6 = "y012345678912ABCDEFGH"                                                 #Codigo de Barra CODE39

    LINECLOSE = "81" + "0" + "Fin de uso."                          #Información  de PLU: Tasa Ampliada, cantidad 1, monto 0.10 bs, nombre del PLU


    #PASO 3: Instanciar la libreria y definir los parametros por defecto que utilizaremos
    Printer = TfhkaPyGD.Tfhka()
    PORT = "COM3";                                                  # Definimos el puerto serial donde esta conectada la impresora fiscal
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


              Respuesta = Printer.SendCmd(FLAG_3001)
              if not Respuesta: print("!!! Comando No Aceptado: " + FLAG_3001)
              else: print("*** Comando Enviado: " + FLAG_3001)

              Respuesta = Printer.SendCmd(FLAG_4303)
              if not Respuesta: print("!!! Comando No Aceptado: " + FLAG_4303)
              else: print("*** Comando Enviado: " + FLAG_4303)

              Respuesta = Printer.SendCmd(LINE1)
              if not Respuesta: print("!!! Comando No Aceptado: " + LINE1)
              else: print("*** Comando Enviado: " + LINE1)
            
              Respuesta = Printer.SendCmd(LINE2)
              if not Respuesta: print("Comando No Aceptado: " + LINE2)
              else: print("*** Comando Enviado: " + LINE2)

              Respuesta = Printer.SendCmd(LINE3)
              if not Respuesta: print("Comando No Aceptado: " + LINE3)
              else: print("*** Comando Enviado: " + LINE3)

              Respuesta = Printer.SendCmd(LINE4)
              if not Respuesta: print("Comando No Aceptado: " + LINE4)
              else: print("*** Comando Enviado: " + LINE4)

              Respuesta = Printer.SendCmd(LINE5)
              if not Respuesta: print("Comando No Aceptado: " + LINE5)
              else: print("*** Comando Enviado: " + LINE5)

              Respuesta = Printer.SendCmd(LINE6)
              if not Respuesta: print("Comando No Aceptado: " + LINE6)
              else: print("*** Comando Enviado: " + LINE6)            

              Respuesta = Printer.SendCmd(LINECLOSE)
              if not Respuesta: print("Comando No Aceptado: " + LINECLOSE)
              else: print("*** Comando Enviado: " + LINECLOSE)
            
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