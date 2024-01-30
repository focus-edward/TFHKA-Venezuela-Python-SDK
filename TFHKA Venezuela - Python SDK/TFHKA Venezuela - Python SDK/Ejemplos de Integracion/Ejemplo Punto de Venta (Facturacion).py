from Libreria import TfhkaPyGD
import time


class EjemploPOS():
    FLAG_2100 = "PJ2100"                                    # Flag para montos por defecto
    FLAG_2801 = "PJ2801"                         
    FLAG_5001 = "PJ5001"                                    # Flag para activar IGTF

    COMMAND_ANULACION= "7"

    RIF = "iR*J-312171197"                                  # Información del Registro de Identficación Fiscal
    SOCIAL_REASON = "iS*THE FACTORY HKA, C.A."              # Información de Razón Social
    ADDRESS_LINE1 = "i00DIRECCION: LA CALIFORNIA"           # Información de Dirección linea 1
    ADDRESS_LINE2 = "i01CARACAS"                            # Información de Dirección linea 2

    PLU1 = " 000000100000001000Producto 1"                  # Información  de PLU: Tasa Exento  , cantidad 1, monto 0.10 bs, nombre del PLU
    PLU2 = "!000000100000001000Producto 2"                  # Información  de PLU: Tasa General , cantidad 1, monto 0.10 bs, nombre del PLU
    PLU3 = '"000000100000001000Producto 3'                  # Información  de PLU: Tasa Reducida, cantidad 1, monto 0.10 bs, nombre del PLU
    PLU4 = "#000000100000001000Producto 4"                  # Información  de PLU: Tasa Ampliada, cantidad 1, monto 0.10 bs, nombre del PLU
    PLU5 = " 000000100000001000Producto 5"                 

    COMMAND_SUBTOTAL = "3"                                  # Comando de subtotal de factura

    COMMAND_PAGOPARCIAL_FIRST = "201000000000010"           # Información del medio de pago: comando 2, medio de pago 01, monto 20.00 bs
    COMMAND_PAGOPARCIAL_SEC =   "203000000000010"           # Comando del Segundo Pago Parcial Factura

    COMMAND_PAGOPARCIAL_01 = "201000000002000"              #Información del medio de pago: comando 2, medio de pago 01, monto 20.00 bs
    COMMAND_PAGOPARCIAL_02 = "202000000001000"              #Información del medio de pago: comando 2, medio de pago 02, monto 10.00 bs
    COMMAND_PAGOPARCIAL_20 = "220000000002000"              #Información del medio de pago: comando 2, medio de pago 20, monto 20.00 bs
    COMMAND_PAGOPARCIAL_21 = "221000000001000"              #Información del medio de pago: comando 2, medio de pago 21, monto 10.00 bs

    COMMAND_PAGOTOTAL = "101"                               # Comando de Totalizar Factura
    COMMAND_CLOSEINVOCE = "199"
    COMMAND_COMMENT = "@EJEMPLO DE POS"                     #Comando envio para Introducir un comentario


    port = "COM3"
    printer = TfhkaPyGD.Tfhka()

    def status_description(status):
        match str(status):
            case "12":
                return 'En modo fiscal, carga completa de la memoria fiscal y emisión de documentos no fiscales'
            case "11":            
                return 'En modo fiscal, carga completa de la memoria fiscal y emisión de documentos fiscales'
            case "10":
                return 'En modo fiscal, carga completa de la memoria fiscal y en espera'
            case "9 ":
                return 'En modo fiscal, cercana carga completa de la memoria fiscal y en emisión de documentos no fiscales'
            case "8 ":
                return 'En modo fiscal, cercana carga completa de la memoria fiscal y en emisión de documentos no fiscales'
            case "7 ":
                return 'En modo fiscal, cercana carga completa de la memoria fiscal y en espera'
            case "6 ":
                return 'En modo fiscal y en emisión de documentos no fiscales'
            case "5 ":
                return 'En modo fiscal y en emisión de documentos fiscales'
            case "4 ":
                return 'En modo fiscal y en espera'
            case "3 ":
                return 'En modo prueba y en emisión de documentos no fiscales'
            case "2 ":
                return 'En modo prueba y en emisión de documentos fiscales'
            case "1 ":
                return 'En modo prueba y en espera'
            case "0 ":
                return 'Status Desconocido'
            case _:
                return 'Status Desconocido'  # Tratamiento por defecto
        
    def send_pago(printer, amount, anul, sleep, cont_pagos, ValueContadorLineas):
        try:
            b_resp = False
            time.sleep(sleep)
            b_resp = printer.SendCmd(amount)

            if b_resp:
                cont_pagos += 1
                print("Comando Enviado: " + amount)
                return True
            else:
                if cont_pagos == ValueContadorLineas:
                    # Comando aceptado.
                    cont_pagos += 1
                    return True
                elif cont_pagos > ValueContadorLineas:
                    # Se reenvía el comando.
                    time.sleep(sleep)
                    b_resp = printer.SendCmd(amount)
                    if b_resp:
                        cont_pagos += 1
                        print("Comando Enviado: " + amount)
                        return True
                    else:
                        # Hubo un problema.
                        print("Comando No Aceptado: " + amount)
                        return False
                else:
                    # Caso en el que se duplicó un pago, se decide si anular transacción o anular pago.
                    # Para este ejemplo, se anuló la transacción.
                    time.sleep(sleep)
                    b_resp = printer.SendCmd(anul)
                    if b_resp:
                        print("Comando Enviado: " + anul)
                    else:
                        print("Comando No Aceptado: " + anul)
                    return False
        except Exception:
            return False
        
    def send_plu(printer, plu, anul, sleep, cont_impresora_fiscal, valueContadorLineas):
        try:
            BRESP = False
            time.sleep(sleep)
            BRESP = printer.SendCmd(plu)
            
            if BRESP:
                cont_impresora_fiscal += 1
                print("Comando Enviado:", plu)
                return True
            else:

                if cont_impresora_fiscal == valueContadorLineas:
                    cont_impresora_fiscal[0] += 1
                    print("Comando Enviado:", plu)
                    return True
                elif cont_impresora_fiscal > valueContadorLineas:
                    time.sleep(sleep)
                    BRESP = printer.SendCmd(plu)

                    if BRESP:
                        cont_impresora_fiscal += 1
                        print("Comando Enviado:", plu)
                        return True
                    else:
                        print("Comando No Aceptado:", plu)
                        return False
                else:
                    time.sleep(sleep)
                    BRESP = printer.SendCmd(anul)
                    
                    if BRESP:
                        print("Comando Enviado:", anul)
                    else:
                        print("Comando No Aceptado:", anul)
                    return False
        except Exception:
            return False


    try:
        PORTOPEN = printer.OpenFpctrl(port)
        if PORTOPEN:
            print("PUERTO:", port, "ABIERTO\n")

            input("Presione la tecla Enter para continuar...\n")
            STATUSPRINTER = printer.ReadFpStatus()
            printer_s = STATUSPRINTER[0]
            match printer_s:
                case "5"|"6"|"2"|"3":
                    TRANS_CURSO = True
                    while TRANS_CURSO:
                        print("############################################################")
                        print("EXISTE UN TRANSSACIÓN EN CURSO")
                        print("¿Desea Anular la transación?:")
                        print("\ta - Si")
                        print("\tb - NO")
                        choice = input("Elija su opción: ")
                        match choice:
                            case "a":
                                BRESP = printer.SendCmd(COMMAND_ANULACION)
                                if BRESP:
                                    print("Comando Enviado: Transación anulada")
                                    TRANS_CURSO = False
                                    break
                                else:
                                    print("Comando No Aceptado: Transación anulada")
                                    TRANS_CURSO = True
                            case "b":
                                print("*** Debe anular la transacción para continuar")
                                TRANS_CURSO = True
                                break
                            case _:
                                TRANS_CURSO = True
                                print("Debe seleccionar una opción válida.")
                case _:
                    TRANS_CURSO = False

            if not TRANS_CURSO:
                print("############################################################")
                INFOPRINTER = printer.GetSVPrinterData()
                print("INFORMACIÓN IMPRESORA FISCAL")
                print("Modelo de Impresora:", INFOPRINTER._pmodel)

                STATUS_ERROR = printer.ReadFpStatus()
                print("Código de Estatus:", STATUS_ERROR[0:2])
                status_descrip = status_description(STATUS_ERROR[0:2])
                print("Descripción del Estatus:", status_descrip)
                print("Código de Error:", STATUS_ERROR[5:10])
                print("Descripción del Error:", STATUS_ERROR[11:])

                STATUSS3 = printer.GetS3PrinterData()

                flag_21 = str(STATUSS3._systemFlags[21])
                flag_28 = str(STATUSS3._systemFlags[28])
                flag_50 = str(STATUSS3._systemFlags[50])


                print("Flag 21:", flag_21, "Montos Máximos permitidos")
                print("Flag 28:", flag_28, "Información referente acumuladores")
                print("Flag 50:", flag_50, "IGTF")

                print("############################################################")
                input("Presione la tecla Enter para cerrar...")

                if flag_21 != "00" or flag_28 != "01" or flag_50 != "01":
                    print("############################################################")
                    print("CONFIGURANDO IMPRESORA FISCAL")
                    if not flag_21 == "00":
                        BRESP = printer.SendCmd(FLAG_2100)
                        if not BRESP:
                            print("No se pudo configurar el Flag 21")
                        else:
                            print("Flag 21:", "Montos Máximos permitidos 8 enteros y 2 decimales")
                    if not flag_28 == "01":
                        BRESP = printer.SendCmd(FLAG_2801)
                        if not BRESP:
                            print("No se pudo configurar el Flag 28")
                        else:
                            print("Flag 28:", "Información referente acumuladores Activado")
                    if not flag_50 == "01":
                        BRESP = printer.SendCmd(FLAG_5001)
                        if not BRESP:
                            print("No se pudo configurar el Flag 50")
                        else:
                            print("Flag 50:", "IGTF Activado")

                    STATUSS3 = printer.GetS3PrinterData()

                    flag_21 = STATUSS3._systemFlags[21]
                    flag_28 = STATUSS3._systemFlags[28]
                    flag_50 = STATUSS3._systemFlags[50]

                    print("############################################################")
                    input("Presione la tecla Enter para continuar...")

                BRESP = printer.SendCmd(SOCIAL_REASON)
                if not BRESP: 
                    print ("Comando No Aceptado: " + SOCIAL_REASON)
                else:
                    ("*** Comando Enviado: " + SOCIAL_REASON)

                BRESP = printer.SendCmd(RIF)
                if not BRESP:
                    ("Comando No Aceptado: " + RIF)
                else:
                        ("*** Comando Enviado: " + RIF)

                BRESP = printer.SendCmd(ADDRESS_LINE1);
                if not BRESP:
                    ("Comando No Aceptado: " + ADDRESS_LINE1)
                else:
                    print ("*** Comando Enviado: " + ADDRESS_LINE1)

                BRESP = printer.SendCmd(ADDRESS_LINE2);
                if not BRESP:
                    ("Comando No Aceptado: " + ADDRESS_LINE2)
                else:
                    ("*** Comando Enviado: " + ADDRESS_LINE2)

                BRESP = printer.SendCmd(COMMAND_COMMENT)

                if not BRESP:
                    ("Comando No Aceptado: " + COMMAND_COMMENT)
                else:
                    print ("*** Comando Enviado: " + COMMAND_COMMENT)

                TRANS_PAGO = False
                TRANS_PLU = True
                contImpresoraFiscal = 0
                STATUSS2 = printer.GetS2PrinterData()
                valueContadorLineas = STATUSS2._quantityArticles

                while TRANS_PLU:
                    print ("")
                    print ("############################################################")
                    print ("SELECCIONE UN PRODUCTO:")
                    print ("\ta - Producto Tasa    Exento, Monto: 10 bs, Cantidad: 1")
                    print ("\tb - Producto Tasa   General, Monto: 10 bs, Cantidad: 1")
                    print ("\tc - Producto Tasa  Reducida, Monto: 10 bs, Cantidad: 1")
                    print ("\td - Producto Tasa  Ampliada, Monto: 10 bs, Cantidad: 1")
                    print ("\te - Producto Tasa Percibido, Monto: 10 bs, Cantidad: 1")
                    print ("\tf - Subtotal")
                    print ("\tg - Pago Total")
                    print ("\th - Pago parcial")
                    print ("\ti - Anular Transaccion")
                    print ("Elija su opcion:")
                    seleccion = input("")
                    match seleccion:                       
                        case "a":
                            TRANS_PLU = send_plu(printer,PLU1,COMMAND_ANULACION,0.1,contImpresoraFiscal,valueContadorLineas)                                                                                          
                        case "b":
                            TRANS_PLU = send_plu(printer,PLU2,COMMAND_ANULACION,0.1,contImpresoraFiscal,valueContadorLineas)                                                                                                                                      
                        case "c":
                            TRANS_PLU = send_plu(printer,PLU3,COMMAND_ANULACION,0.1,contImpresoraFiscal,valueContadorLineas)                                                                                                                          
                        case "d":
                            TRANS_PLU = send_plu(printer,PLU4,COMMAND_ANULACION,0.1,contImpresoraFiscal,valueContadorLineas)                                                                                                                   
                        case "e":
                            TRANS_PLU = send_plu(printer,PLU5,COMMAND_ANULACION,0.1,contImpresoraFiscal,valueContadorLineas)                                                                                                                                                        
                        case "f":
                            TRANS_PLU = printer.SendCmd(COMMAND_SUBTOTAL)
                            time.sleep(0.1)
                            if not TRANS_PLU:
                                print ("Comando no aceptado:"+COMMAND_SUBTOTAL)
                            else:
                                print ("Comando Enviado:"+COMMAND_SUBTOTAL)    
                        case "g":
                            TRANS_PLU = not printer.SendCmd(COMMAND_PAGOTOTAL)
                            time.sleep(0.1)
                            if not TRANS_PLU:
                                print ("Comando Enviado:"+COMMAND_PAGOTOTAL)
                                TRANS_PLU = not printer.SendCmd(COMMAND_CLOSEINVOCE)
                                print ("Comando Enviado:"+COMMAND_CLOSEINVOCE)
                            else:
                                print ("Comando no aceptado:"+COMMAND_PAGOTOTAL)
                                TRANS_PLU = not printer.SendCmd(COMMAND_ANULACION)   
                                print ("Comando Enviado:"+COMMAND_ANULACION)                            
                        case "h":
                            TRANS_PLU = False
                            TRANS_PAGO = True
                        case "i":
                            TRANS_PLU = not printer.SendCmd(COMMAND_ANULACION)
                            time.sleep(0.1)
                            if not TRANS_PLU:
                                print ("Comando no aceptado:"+COMMAND_ANULACION)
                            else:
                                print ("Comando Enviado:"+COMMAND_ANULACION)                             
                        case _:
                            print ("Debe seleccionar una opción valida.")

                amountTotalBases = 0                
                amountTax = 0
                amountTotal = 0

                amountPagar = 0.0
                amountPagado = 0.0

                change = 0.0
                contPagos = 0

                while TRANS_PAGO:
                    
                    STATUSS2 = printer.GetS2PrinterData()
                    amountTotalBases = STATUSS2._subTotalBases
                    amountPagar = STATUSS2._amountPayable
                    amountTax = STATUSS2._subTotalTax
                    TRANS_PAGO = bool(STATUSS2)
                    contPagos = 0
                    valueContadorLineas = STATUSS2._numberPaymentsMade
                    if TRANS_PAGO:
                    
                        if contPagos == 0:
                            amountTotal = amountTotalBases + amountTax

                        if amountPagar > 0:
                        

                            print ("")
                            print ("################################amount############################")
                            print ("BASE IMPONIBLE: Bs.",amountTotalBases," SUBTOTAL IMPUESTOS: Bs.",amountTax)
                            print ("MONTO A PAGAR: Bs.",amountPagar)
                            print ("############################################################")
                            print ("SELECCIONE UN MEDIO DE PAGO:")
                            print ("\ta - Medio de Pago 01 Monto: 20 bs, No aplica IGFT ")
                            print ("\tb - Medio de Pago 02 Monto: 10 bs, No aplica IGFT")
                            print ("\tc - Medio de Pago 20 Monto: 20 bs, Aplica IGFT")
                            print ("\td - Medio de Pago 21 Monto: 10 bs, Aplica IGFT")
                            print ("\te - Pago Total")
                            print ("\tf - Anular Transaccion")
                            print ("Elija su opcion:")
                            pago = input("")

                            match pago:
                            
                                case "a":
                                    TRANS_PAGO = send_pago(printer,COMMAND_PAGOPARCIAL_01, COMMAND_ANULACION, 0.1, contPagos, valueContadorLineas )
                                    time.sleep(0.1)
                                    if amountPagar >= 20:
                                        amountPagado += 20 
                                        contPagos += 1
                                    else:
                                        change = 20 - amountPagar
                                case "b":
                                    TRANS_PAGO = printer.SendCmd(COMMAND_PAGOPARCIAL_02)
                                    time.sleep(0.1)
                                    if amountPagar >= 10:
                                        amountPagado += 10
                                        contPagos += 1
                                    else:
                                        change = (10 - amountPagar)
                                case "c":
                                    TRANS_PAGO = send_pago(printer,COMMAND_PAGOPARCIAL_20, COMMAND_ANULACION, 0.1, contPagos, valueContadorLineas )
                                    if amountPagar >= 20:
                                        amountPagado += 20 + (20 * 0.03)
                                        contPagos += 1
                                    else:
                                        change = (20 - (amountPagar * 1.03))
                                case "d":
                                    TRANS_PAGO = send_pago(printer,COMMAND_PAGOPARCIAL_21, COMMAND_ANULACION, 0.1, contPagos, valueContadorLineas )
                                    contPagos += 1
                                    if amountPagar >= 10:
                                        amountPagado += 10 
                                    else:
                                        change = (10 - (amountPagar * 1.03))
                                case "e":
                                    TRANS_PAGO = not printer.SendCmd(COMMAND_PAGOTOTAL)
                                    time.sleep(0.1)
                                    if not TRANS_PAGO:
                                        TRANS_PAGO = not printer.SendCmd(COMMAND_CLOSEINVOCE)
                                        time.sleep(0.1)
                                    else:
                                        TRANS_PAGO = not printer.SendCmd(COMMAND_ANULACION)
                                        time.sleep(0.1)
                                        print ("Comando Enviado:"+COMMAND_ANULACION+"Transación anulada")
                                case "f":
                                    TRANS_PAGO = not printer.SendCmd(COMMAND_ANULACION)
                                    time.sleep(0.1)
                                case _:
                                    print("Debe seleccionar una opción valida.")
                        else:
                                print("")
                                print("############################################################")
                                print(f"CAMBIO: Bs.{change}")
                                print("############################################################")
                                print("")   

                                TRANS_PAGO = not printer.SendCmd(COMMAND_CLOSEINVOCE)
                                time.sleep(0.1)                                                                  
                                if TRANS_PAGO:
                                    print ("Comando No Aceptado: " + COMMAND_CLOSEINVOCE)
                                else:
                                    print ("*** Comando Enviado: " + COMMAND_CLOSEINVOCE)   
                print("")
                print("############################################################")
                print("FACTURA TERMINADA")
                print("############################################################")
                print("")

                print("Presione la tecla Enter para cerrar...")
                input()

        else:
            print("NO SE PUDO ESTABLECER COMUNICACION CON LA IMPRESORA")
            print(f"PUERTO: {port} CERRADO")

            print("")
            print("############################################################")
            print("")

            print("Presione la tecla Enter para cerrar...")
            input()            


    except Exception as ex:
        print("OCURRIO UNA EXCEPCION:\nDetalles del Error:\n\"{}\"\n".format(str(ex)))

        print("")
        print("############################################################")
        print("")

        print("Presione la tecla Enter para cerrar...")
        input()









