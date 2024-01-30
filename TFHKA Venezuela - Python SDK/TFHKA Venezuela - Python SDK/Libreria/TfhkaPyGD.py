# ESTA LIBRERIA TIENE TODAS LAS CLASES INTERNAS

from functools import reduce
import serial
import operator
import time
import datetime
from tokenize import Double



class port:
  portName = "COM12" #Changed by p
  baudRate =9600
  dataBits =serial.EIGHTBITS
  stopBits =serial.STOPBITS_ONE
  parity =serial.PARITY_EVEN
  readBufferSize =256
  writeBufferSize =256
  readTimeOut=1.0
  writeTimeOut=5.0
class tf_ve_ifpython:
  __version__ = "2.0.1"
  bandera=False
  mdepura=False
  status =''
  envio  =''
  error  =''
  ##
  Port=port()


#Funcion ABRIR
  def OpenFpctrl(self, p):
    if not self.bandera:
      try:
        self.ser=serial.Serial(port=p, baudrate=self.Port.baudRate, bytesize=self.Port.dataBits, parity=self.Port.parity, stopbits=self.Port.stopBits, timeout=self.Port.readTimeOut, writeTimeout=self.Port.writeTimeOut, xonxoff=True, rtscts=True, dsrdtr=True)
        #Find out what are xonxoff, and rtscts for
        print ("CTS", self.ser.cts)
        print ("RTS", self.ser.rts)
        print ("DSR", self.ser.dsr)
        print ("DTR", self.ser.dtr)
        self.bandera=True
        return True
      except (serial.PortNotOpenError, serial.SerialTimeoutException, serial.SerialException):
        self.bandera = False
        return False

#Funcion CERRAR
  def CloseFpctrl(self):
    if self.bandera:
      self.ser.close()
      self.bandera=False
      return self.bandera

#Funcion MANIPULA
  def _HandleCTSRTS(self):
    try:
      self.ser.setRTS(True)
      lpri=1
      while not self.ser.getCTS():
        lpri=lpri+1
        if lpri>20:
          self.ser.setRTS(False)
          return False
      return True
    except:
      return False

  def SendCmd(self,cmd):
    #time.sleep(0.30)
    if cmd == "I0X" or cmd == "I1X" or cmd == "I1Z":
      time.sleep(1)
      self.trama = self._States_Report(cmd,4)

      return self.trama
    if cmd == "I0Z":
      time.sleep(1)
      self.trama = self._States_Report(cmd,9)
      return self.trama   
    else:
      
      try:
        self.ser.flushInput()
        self.ser.flushOutput()
        if self._HandleCTSRTS():
          msj=self._AssembleQueryToSend(cmd)
          self._write(msj.encode("iso-8859-1"))
          max_attempts=5
          contador=0
          rt=self._read(1)
          while rt == (b'') and contador < max_attempts:
            contador += 1
            time.sleep(0.2)
            rt = self._read(1)

          if rt.decode()==chr(0x06):
            self.envio = "Status: 00  Error: 00"
            rt=True
          else:
            self.envio = "Status: 00  Error: 89"
            rt=False
        else:
          self._GetStatusError(0, 128)
          self.envio = "Error... CTS in False"
          rt=False
        self.ser.setRTS(False)
      except serial.SerialException:
        rt=False
      return rt

  def SendCmdFile(self, cmd):
    f = open(cmd, encoding='iso-8859-1')      
    for linea in f:
       if (linea!=""):
          linea = linea.rstrip()
          self.SendCmd(linea)

  def _QueryCmd(self,cmd):
      try:
         self.ser.flushInput()
         self.ser.flushOutput()
         if self._HandleCTSRTS():
            msj=self._AssembleQueryToSend(cmd)
            self._write(msj.encode())
            rt=True
         else:
            self._GetStatusError(0, 128)
            self.envio = "Error... CTS in False"
            rt=False
            self.ser.setRTS(False)
      except serial.SerialException:
         rt=False
      return rt

  def _FetchRow(self):
    while True:
      time.sleep(1)
      bytes = self.ser.inWaiting()
      linea=None
      if bytes>1:
        msj=self._read(bytes)
        linea=msj[1:-1]
        lrc=self._Lrc(linea)
        #print ("este es el ejemplo:" + str(linea))
        return linea
      else:
        break
    return linea

  def _FetchRow_Report(self, r):
    while True:
      time.sleep(r)
      bytes = self.ser.inWaiting()
      if bytes>0:
        msj=self._read(bytes)
        linea=msj
        lrc=self._Lrc(linea)
        if lrc==msj:
          self.ser.flushInput()
          self.ser.flushOutput()
          return msj
        else:
          return msj
          break
      else:
        break
    return None

  def ReadFpStatus(self):
    if self._HandleCTSRTS():
      msj=chr(0x05)
      self._write(msj.encode())
      time.sleep(0.05)
      r=self._read(5)
      if len(r)==5:
        if r[1]^r[2]^0x03 == r[4]:
          return self._GetStatusError(r[1], r[2])
        else:
          return self._GetStatusError(0, 144)
      else:
        return self._GetStatusError(0, 114)
    else:
      return self._GetStatusError(0, 128);

  def _write(self,msj):
    if self.mdepura:
      print +self._Debug(msj)
    self.ser.write(msj)

  def _read(self,bytes):
    msj = self.ser.read(bytes)
    if self.mdepura:
      print +self._Debug(msj)
    return msj

  def _AssembleQueryToSend(self,linea):
    lrc = self._Lrc(linea+chr(0x03))
    previo=chr(0x02)+linea+chr(0x03)+chr(lrc)
    return previo

  def _Lrc(self,linea):
    return reduce(operator.xor, map(ord, str(linea)))

  def _Debug(self,linea):
    if linea!=None:
      if len(linea)==0:
        return 'null'
      if len(linea)>3:
        lrc=linea[-1]
        linea=linea[0:-1]
        adic='LRC('+str(lrc)+')'
      else:
        adic=''
      linea=linea.replace('STX',chr(0x02),1)
      linea=linea.replace('ENQ',chr(0x05),1)
      linea=linea.replace('ETX',chr(0x03),1)
      linea=linea.replace('EOT',chr(0x04),1)
      linea=linea.replace('ACK',chr(0x06),1)
      linea=linea.replace('NAK',chr(0x15),1)
      linea=linea.replace('ETB',chr(0x17),1)

    return linea+adic

  def _States(self, cmd):
    #print (self)
    self._QueryCmd(cmd)
    while True:
      trama=self._FetchRow()
      #print ("trama del STADO: "+ str(trama))
      return trama

  def _States_Report(self, cmd, r):
    #print cmd
    ret = r
    self._QueryCmd(cmd)
    while True:
      time.sleep(2)
      trama=self._FetchRow_Report(ret)
      #print "La trama es", trama, "hasta aca"
      if trama==None:
        break
      return trama

  def _UploadDataReport(self, cmd):
    msj=""
    arreglodemsj=[]
    counter=0
    try:
      self.ser.flushInput()
      self.ser.flushOutput()
      if self._HandleCTSRTS():
         m=""
         msj=self._AssembleQueryToSend(cmd)
         self._write(msj.encode())
         rt=self._read(1)
         while True:
            while msj!= chr(0x04):
               
               time.sleep(0.5)
               msj=self._Debug('ACK')
               self._write(msj.encode())
               time.sleep(0.5)
               
               msj=self._FetchRow_Report(1.3)
               #print ("trama del MSJ 2: "+ str(msj))
               if(msj==None):
                 break
               else:
                 arreglodemsj.append(msj)
            return arreglodemsj
      else:
         self._GetStatusError(0, 128)
         self.envio = "Error... CTS in False"
         m=None
         self.ser.setRTS(False)
    except serial.SerialException:
       m=None
    return m

  def _ReadFiscalMemoryByNumber(self, cmd):
    msj=""
    arreglodemsj=[]
    counter=0
    try:
      self.ser.flushInput()
      self.ser.flushOutput()
      if self._HandleCTSRTS():
         m=""
         msj=self._AssembleQueryToSend(cmd)
         self._write(msj.encode())
         rt=self._read(1)
         while True:
            while msj!= chr(0x04):
               time.sleep(0.5)
               msj=self._Debug('ACK')
               self._write(msj.encode())
               time.sleep(0.5)
               msj=self._FetchRow_Report(1.3)
               if(msj==None):
                 break
               else:
                 arreglodemsj.append(msj)
            return arreglodemsj
      else:
         self._GetStatusError(0, 128);
         self.envio = "Error... CTS in False"
         m=None
         self.ser.setRTS(False)
    except serial.SerialException:
       m=None
    return m

  def _ReadFiscalMemoryByDate(self, cmd):
    msj=""
    arreglodemsj=[]
    counter=0
    try:
      self.ser.flushInput()
      self.ser.flushOutput()
      if self._HandleCTSRTS():
         m=""
         msj=self._AssembleQueryToSend(cmd)
         self._write(msj.encode())
         rt=self._read(1)
         while True:
            while msj!= chr(0x04):
               time.sleep(0.5)
               msj=self._Debug('ACK')
               self._write(msj.encode())
               time.sleep(0.5)
               msj=self._FetchRow_Report(1.5)
               if(msj==None):
                 break
               else:
                 arreglodemsj.append(msj)
            return arreglodemsj
      else:
         self._GetStatusError(0, 128);
         self.envio = "Error... CTS in False"
         m=None
         self.ser.setRTS(False)
    except serial.SerialException:
       m=None
    return m

  def _GetStatusError(self,st,er):
    st_aux = st;
    st = st & ~0x04

    if   (st & 0x6A) == 0x6A: #En modo fiscal, carga completa de la memoria fiscal y emisi�n de documentos no fiscales
      self.status='En modo fiscal, carga completa de la memoria fiscal y emisi�n de documentos no fiscales'
      status = "12"
    elif (st & 0x69) == 0x69: #En modo fiscal, carga completa de la memoria fiscal y emisi�n de documentos  fiscales
      self.status='En modo fiscal, carga completa de la memoria fiscal y emisi�n de documentos  fiscales'
      status = "11"
    elif (st & 0x68) == 0x68: #En modo fiscal, carga completa de la memoria fiscal y en espera
      self.status='En modo fiscal, carga completa de la memoria fiscal y en espera'
      status = "10"
    elif (st & 0x72) == 0x72: #En modo fiscal, cercana carga completa de la memoria fiscal y en emisi�n de documentos no fiscales
      self.status='En modo fiscal, cercana carga completa de la memoria fiscal y en emisi�n de documentos no fiscales'
      status = "9 "
    elif (st & 0x71) == 0x71: #En modo fiscal, cercana carga completa de la memoria fiscal y en emisi�n de documentos no fiscales
      self.status='En modo fiscal, cercana carga completa de la memoria fiscal y en emisi�n de documentos no fiscales'
      status = "8 "
    elif (st & 0x70) == 0x70: #En modo fiscal, cercana carga completa de la memoria fiscal y en espera
      self.status='En modo fiscal, cercana carga completa de la memoria fiscal y en espera'
      status = "7 "
    elif (st & 0x62) == 0x62: #En modo fiscal y en emisi�n de documentos no fiscales
      self.status='En modo fiscal y en emisi�n de documentos no fiscales'
      status = "6 "
    elif (st & 0x61) == 0x61: #En modo fiscal y en emisi�n de documentos fiscales
      self.status='En modo fiscal y en emisi�n de documentos fiscales'
      status = "5 "
    elif (st & 0x60) == 0x60: #En modo fiscal y en espera
      self.status='En modo fiscal y en espera'
      status = "4 "
    elif (st & 0x42) == 0x42: #En modo prueba y en emisi�n de documentos no fiscales
      self.status='En modo prueba y en emisi�n de documentos no fiscales'
      status = "3 "
    elif (st & 0x41) == 0x41: #En modo prueba y en emisi�n de documentos fiscales
      self.status='En modo prueba y en emisi�n de documentos fiscales'
      status = "2 "
    elif (st & 0x40) == 0x40: #En modo prueba y en espera
      self.status='En modo prueba y en espera'
      status = "1 "
    elif (st & 0x00) == 0x00: #Status Desconocido
      self.status='Status Desconocido'
      status = "0 "

    if   (er & 0x6C) == 0x6C: #Memoria Fiscal llena
      self.error = 'Memoria Fiscal llena'
      error = "108"
    elif (er & 0x64) == 0x64: #Error en memoria fiscal
      self.error = 'Error en memoria fiscal'
      error = "100"
    elif (er & 0x60) == 0x60: #Error Fiscal
      self.error = 'Error Fiscal'
      error = "96 "
    elif (er & 0x5C) == 0x5C: #Comando Invalido
      self.error = 'Comando Invalido'
      error = "92 "
    elif (er & 0x58) == 0x58: # No hay asignadas  directivas
      self.error = 'No hay asignadas  directivas'
      error = "88 "
    elif (er & 0x54) == 0x54: #Tasa Invalida
      self.error = 'Tasa Invalida'
      error = "84 "
    elif (er & 0x50) == 0x50: #Comando Invalido/Valor Invalido
      self.error = 'Comando Invalido/Valor Invalido'
      error = "80 "
    elif (er & 0x43) == 0x43: #Fin en la entrega de papel y error mec�nico
      self.error = 'Fin en la entrega de papel y error mec�nico'
      error = "3  "
    elif (er & 0x42) == 0x42: #Error de indole mecanico en la entrega de papel
      self.error = 'Error de indole mecanico en la entrega de papel'
      error = "2  "
    elif (er & 0x41) == 0x41: #Fin en la entrega de papel
      self.error = 'Fin en la entrega de papel'
      error = "1  "
    elif (er & 0x40) == 0x40: #Sin error
      self.error = 'Sin error'
      error = "0  "

    if (st_aux & 0x04) == 0x04: #Buffer Completo
      self.error = ''
      error = "112 "
    elif er == 128:     # Error en la comunicacion
      self.error = 'CTS en falso'
      error = "128 ";
    elif er == 137:     # No hay respuesta
      self.error = 'No hay respuesta'
      error = "137 ";
    elif er == 144:     # Error LRC
      self.error = 'Error LRC'
      error = "144 ";
    elif er == 114:
      self.error = 'Impresora no responde o ocupada'
      error = "114 ";
    return status+"   " +error+"   " +self.error
class Tfhka(tf_ve_ifpython):

  def GetSVPrinterData(self):
    self.trama=self._States("SV")
    #print self.trama
    self.SVPrinterData = SVPrinterData(self.trama)
    #print self.S1PrinterData
    return self.SVPrinterData
  
  """ def GetPrinterStatus(self):
    self.trama=self._States("SV")
    #print self.trama
    self.SVPrinterData = PrinterStatus(self.trama)
    #print self.S1PrinterData
    return self.SVPrinterData """

  def GetS1PrinterData(self):
    self.trama=self._States("S1")
    #print self.trama
    self.S1PrinterData = S1PrinterData(self.trama)
    #print self.S1PrinterData
    return self.S1PrinterData

  def GetS2PrinterData(self):
    self.trama=self._States("S2")
    self.S2PrinterData= S2PrinterData(self.trama)
    return self.S2PrinterData
    

  def GetS3PrinterData(self):
    self.trama=self._States("S3")
    #print self.trama
    self.S3PrinterData= S3PrinterData(self.trama)
    return self.S3PrinterData
  
  def GetS4PrinterData(self):
    self.trama=self._States("S4")
    #print self.trama
    self.S4PrinterData= S4PrinterData(self.trama)
    return self.S4PrinterData
  
  def GetS5PrinterData(self):
    self.trama=self._States("S5")
    #print self.trama
    self.S5PrinterData= S5PrinterData(self.trama)
    return self.S5PrinterData
  
  def GetS6PrinterData(self):
    self.trama=self._States("S6")
    #print self.trama
    self.S6PrinterData= S6PrinterData(self.trama)
    return self.S6PrinterData
  
  def GetS7PrinterData(self):
    self.trama=self._States("S7")
    #print self.trama
    self.S7PrinterData= S7PrinterData(self.trama)
    return self.S7PrinterData

  def GetS8EPrinterData(self):
    self.trama=self._States("S8E")
    #print self.trama
    self.S8EPrinterData= S8EPrinterData(self.trama)
    return self.S8EPrinterData
  
  def GetS8PPrinterData(self):
    self.trama=self._States("S8P")
    #print self.trama
    self.S8PPrinterData= S8PPrinterData(self.trama)
    return self.S8PPrinterData
  
  def GetXReport(self):
    self.trama=self._UploadDataReport("U0X")
    #print self.trama
    self.XReport=ReportData(self.trama)
  
    return self.XReport

  def GetX2Report(self):
    self.trama=self._UploadDataReport("U1X")
    #print self.trama
    self.XReport=ReportData(self.trama)
    return self.XReport

  def GetX4Report(self):
    self.trama=self._UploadDataReport("U0X4")
    #print self.trama
    self.XReport=AcumuladosX(self.trama)
    return self.XReport

  def GetX5Report(self):
    self.trama=self._UploadDataReport("U0X5")
    #print self.trama
    self.XReport=AcumuladosX(self.trama)
    return self.XReport

  def GetX7Report(self):
    self.trama=self._UploadDataReport("U0X7")
    #print self.trama
    self.XReport=AcumuladosX(self.trama)
    return self.XReport

  def GetZReport(self, *items): #(self, mode, startParam, endParam): #(self, startDate, endDate):
    if(len(items)>0):
      mode=items[0]
      startParam=items[1]
      endParam=items[2]
      if (type(startParam)==datetime.date and type(endParam)==datetime.date):
        starString=startParam.strftime("%d%m%y")
        endString=endParam.strftime("%d%m%y")
        cmd="U2"+mode+starString+endString
        self.trama=self._ReadFiscalMemoryByDate(cmd)
      else:
        starString = str(startParam)
        while (len(starString) < 6):
          starString = "0" + starString
        endString = str(endParam)
        while (len(endString) < 6):
          endString = "0" + endString
        cmd="U3"+mode+starString+endString
        self.trama=self._ReadFiscalMemoryByNumber(cmd)
      self.ReportData=[]
      i=0
      for report in self.trama[0:-1]:
        self.Z=ReportExtra(report)        
        self.ReportData.append(self.Z)
        i+=1
    else:
      self.trama=self._UploadDataReport("U0Z")
      self.ReportData=ReportData(self.trama)       
    return self.ReportData
  
  def PrintXReport(self):
    self.trama = self._States_Report("I0X",9)
    return self.trama
    
  def PrintZReport(self, *items): #(self, mode, startParam, endParam):
    if(len(items)>0):
      mode=items[0]
      startParam=items[1]
      endParam=items[2]

      rep=False

      if (type(startParam)==datetime.date and type(endParam)==datetime.date): #if(type(startParam)==int and (type(endParam)==int)):
        starString=startParam.strftime("%d%m%y")
        endString=endParam.strftime("%d%m%y")
        cmd="I2"+mode+starString+endString
        rep = self.SendCmd("I2" + mode + starString + endString)
      else:
        starString = str(startParam)
        while (len(starString) < 6):
          starString = "0" + starString
        endString = str(endParam)
        while (len(endString) < 6):
          endString = "0" + endString
        rep = self.SendCmd("I3" + mode + starString + endString)
        if (rep==False):
          if (starString > endString):
            estado = "The original number can not be greater than the final number" #raise(Estado)
    else:
      self.trama = self._States_Report("I0Z",9)
      return self.trama

class ReportData(object):

  _numberOfLastZReport = 0
  _zReportDate = ""
  _zReportTime = ""
  _numberOfLastInvoice = 0
  _lastInvoiceDate = ""
  _lastInvoiceTime = ""
  _numberOfLastDebitNote = 0
  _numberOfLastCreditNote = 0
  _numberOfLastNonFiscal = 0

  _freeSalesTax = 0 # ventas
  _generalRate1Sale = 0
  _generalRate1Tax = 0
  _reducedRate2Sale = 0
  _reducedRate2Tax = 0
  _additionalRate3Sal = 0
  _additionalRate3Tax = 0
  _igtfRateSales = 0
  _igtfRateTaxSales = 0
  _persivSales = 0

  _freeTaxDebit = 0 # Notas de Debito
  _generalRateDebit = 0
  _generalRateTaxDebit = 0
  _reducedRateDebit = 0
  _reducedRateTaxDebit = 0
  _additionalRateDebit = 0
  _additionalRateTaxDebit = 0
  _igtfRateDebit = 0
  _igtfRateTaxDebit = 0
  _persivDebit = 0

  _freeTaxDevolution = 0 # Notas de Credito
  _generalRateDevolution = 0
  _generalRateTaxDevolution = 0
  _reducedRateDevolution = 0
  _reducedRateTaxDevolution = 0
  _additionalRateDevolution = 0
  _additionalRateTaxDevolution = 0
  _igtfRateDevolution = 0
  _igtfRateTaxDevolution = 0
  _persivDevolution = 0
  

  def __init__(self, trama):
    if (trama != None):
      #print("longitud 2: "+ str(len(trama[0])))

      if (len(trama[0]) == 638 or len(trama[0]) == 524 ): #FLAG 63:19 - 63:17 - 63:03(SIN IGTF)
        #print("longitud de la trama que accedo: "+ str(len(trama[0])))
        try:
          _arrayParameter=str(trama).split(chr(0X0A))

          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][7:11])
            _hr = _arrayParameter[0][21:23]
            _mn = _arrayParameter[0][23:25]            
            _dd = _arrayParameter[0][17:19]
            _mm = _arrayParameter[0][15:17]
            _aa = int(_arrayParameter[0][13:15])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][27:35])
            _hr = _arrayParameter[0][45:47]
            _mn = _arrayParameter[0][47:49]

            _dd = _arrayParameter[0][41:43]
            _mm = _arrayParameter[0][39:41]
            _aa = int(_arrayParameter[0][37:39])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][61:69])
            self._numberOfLastDebitNote = int(_arrayParameter[0][51:59])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][71:79])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][81:99])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][101:119])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][121:139])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][141:159])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][161:179])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][181:199])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][201:219])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][221:239])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][241:259])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][261:279])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][281:299])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][301:319])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][321:339])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][341:359])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][361:379])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][381:399])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][401:419])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][421:439])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][441:459])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][461:479])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][481:499])

            self._persivSales = Util().DoValueDouble(_arrayParameter[0][501:519])
            self._persivDebit = Util().DoValueDouble(_arrayParameter[0][521:539])
            self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][541:559])

            self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][561:579])
            self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][581:599])
            self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][601:619])
            self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][621:639])
            self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][641:659])
            self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][661:679])
        except (ValueError):
          return
      
      if (len(trama[0]) == 362): #(FLAG 63:00)
        try:
          _arrayParameter=str(trama).split(chr(0X0A))
          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][7:11])
            _hr = _arrayParameter[0][21:23]
            _mn = _arrayParameter[0][23:25]            
            _dd = _arrayParameter[0][17:19]
            _mm = _arrayParameter[0][15:17]
            _aa = int(_arrayParameter[0][13:15])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][27:35])
            _hr = _arrayParameter[0][45:47]
            _mn = _arrayParameter[0][47:49]

            _dd = _arrayParameter[0][41:43]
            _mm = _arrayParameter[0][39:41]
            _aa = int(_arrayParameter[0][37:39])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][61:69])
            self._numberOfLastDebitNote = int(_arrayParameter[0][51:59])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][71:79])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][81:94])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][96:108])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][111:124])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][126:139])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][141:154])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][156:169])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][171:184])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][186:199])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][201:214])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][216:229])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][231:244])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][246:259])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][261:274])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][276:289])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][291:304])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][306:319])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][321:334])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][336:349])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][351:364])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][366:379])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][381:394])

            #self._persivSales = Util().DoValueDouble(_arrayParameter[0][501:519])
            #self._persivDebit = Util().DoValueDouble(_arrayParameter[0][521:539])
            #self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][541:559])
              
            #self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][561:579])
            #self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][581:599])
            #self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][601:619])
            #self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][621:639])
            #self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][641:659])
            #self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][661:679])
        except (ValueError):
          return

    if (len(trama[0]) == 467): #(FLAG 63:01)
        try:
          _arrayParameter=str(trama).split(chr(0X0A))
          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][7:11])
            _hr = _arrayParameter[0][21:23]
            _mn = _arrayParameter[0][23:25]            
            _dd = _arrayParameter[0][17:19]
            _mm = _arrayParameter[0][15:17]
            _aa = int(_arrayParameter[0][13:15])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][27:35])
            _hr = _arrayParameter[0][45:47]
            _mn = _arrayParameter[0][47:49]

            _dd = _arrayParameter[0][41:43]
            _mm = _arrayParameter[0][39:41]
            _aa = int(_arrayParameter[0][37:39])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][61:69])
            self._numberOfLastDebitNote = int(_arrayParameter[0][51:59])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][71:79])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][81:99])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][101:119])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][121:139])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][141:159])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][161:179])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][181:199])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][201:219])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][221:239])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][241:259])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][261:279])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][281:299])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][301:319])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][321:339])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][341:359])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][361:379])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][381:399])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][401:419])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][421:439])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][441:459])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][461:479])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][481:499])

            #self._persivSales = Util().DoValueDouble(_arrayParameter[0][501:519])
            #self._persivDebit = Util().DoValueDouble(_arrayParameter[0][521:539])
            #self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][541:559])
              
            #self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][561:579])
            #self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][581:599])
            #self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][601:619])
            #self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][621:639])
            #self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][641:659])
            #self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][661:679])
        except (ValueError):
          return

    if (len(trama[0]) == 419 or len(trama[0]) == 533): #(FLAG 63:02 - 63:16 - 63:18)
        try:
          _arrayParameter=str(trama).split(chr(0X0A))
          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][7:11])
            _hr = _arrayParameter[0][21:23]
            _mn = _arrayParameter[0][23:25]            
            _dd = _arrayParameter[0][17:19]
            _mm = _arrayParameter[0][15:17]
            _aa = int(_arrayParameter[0][13:15])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][27:35])
            _hr = _arrayParameter[0][45:47]
            _mn = _arrayParameter[0][47:49]

            _dd = _arrayParameter[0][41:43]
            _mm = _arrayParameter[0][39:41]
            _aa = int(_arrayParameter[0][37:39])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][61:69])
            self._numberOfLastDebitNote = int(_arrayParameter[0][51:59])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][71:79])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][81:94])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][96:108])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][111:124])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][126:139])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][141:154])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][156:169])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][171:184])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][186:199])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][201:214])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][216:229])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][231:244])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][246:259])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][261:274])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][276:289])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][291:304])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][306:319])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][321:334])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][336:349])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][351:364])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][366:379])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][381:394])

            self._persivSales = Util().DoValueDouble(_arrayParameter[0][396:414])
            self._persivDebit = Util().DoValueDouble(_arrayParameter[0][416:434])
            self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][436:454])
            
            #FLAG 63:16
            self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][456:474])
            self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][476:494])
            self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][496:514])
            self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][516:534])
            self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][536:554])
            self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][556:574])

            
        except (ValueError):
          return      
class ReportExtra(object):

  _numberOfLastZReport = 0
  _zReportDate = ""
  _zReportTime = ""
  _numberOfLastInvoice = 0
  _lastInvoiceDate = ""
  _lastInvoiceTime = ""
  _numberOfLastDebitNote = 0
  _numberOfLastCreditNote = 0
  _numberOfLastNonFiscal = 0

  _freeSalesTax = 0 # ventas
  _generalRate1Sale = 0
  _generalRate1Tax = 0
  _reducedRate2Sale = 0
  _reducedRate2Tax = 0
  _additionalRate3Sal = 0
  _additionalRate3Tax = 0
  _igtfRateSales = 0
  _igtfRateTaxSales = 0
  _persivSales = 0

  _freeTaxDebit = 0 # Notas de Debito
  _generalRateDebit = 0
  _generalRateTaxDebit = 0
  _reducedRateDebit = 0
  _reducedRateTaxDebit = 0
  _additionalRateDebit = 0
  _additionalRateTaxDebit = 0
  _igtfRateDebit = 0
  _igtfRateTaxDebit = 0
  _persivDebit = 0

  _freeTaxDevolution = 0 # Notas de Credito
  _generalRateDevolution = 0
  _generalRateTaxDevolution = 0
  _reducedRateDevolution = 0
  _reducedRateTaxDevolution = 0
  _additionalRateDevolution = 0
  _additionalRateTaxDevolution = 0
  _igtfRateDevolution = 0
  _igtfRateTaxDevolution = 0
  _persivDevolution = 0
  

  def __init__(self, trama):
    if (trama != None):
      #print("longitud 2: "+ str(len(trama[0])))

      if (len(trama) == 638 or len(trama) == 524 ): #FLAG 63:19 - 63:17 - 63:03(SIN IGTF)
        #print("longitud de la trama que accedo: "+ str(len(trama[0])))
        try:
          _arrayParameter=str(trama).split(chr(0X0A))

          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][6:10])
            _hr = _arrayParameter[0][20:22]
            _mn = _arrayParameter[0][22:24]            
            _dd = _arrayParameter[0][16:18]
            _mm = _arrayParameter[0][14:16]
            _aa = int(_arrayParameter[0][12:14])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][26:34])
            _hr = _arrayParameter[0][44:46]
            _mn = _arrayParameter[0][46:48]

            _dd = _arrayParameter[0][40:42]
            _mm = _arrayParameter[0][38:40]
            _aa = int(_arrayParameter[0][36:38])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][60:68])
            self._numberOfLastDebitNote = int(_arrayParameter[0][50:58])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][70:78])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][80:98])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][100:118])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][120:138])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][140:158])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][160:178])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][180:198])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][200:218])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][220:238])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][240:258])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][260:278])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][280:298])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][300:318])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][320:338])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][340:358])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][360:378])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][380:398])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][400:418])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][420:438])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][440:458])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][460:478])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][480:498])

            self._persivSales = Util().DoValueDouble(_arrayParameter[0][500:518])
            self._persivDebit = Util().DoValueDouble(_arrayParameter[0][520:538])
            self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][540:558])

            self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][560:578])
            self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][580:598])
            self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][600:618])
            self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][620:638])
            self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][640:658])
            self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][660:678])
        except (ValueError):
          return
      
      if (len(trama) == 362): #(FLAG 63:00)
        try:
          _arrayParameter=str(trama).split(chr(0X0A))
          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][6:10])
            _hr = _arrayParameter[0][20:22]
            _mn = _arrayParameter[0][22:24]            
            _dd = _arrayParameter[0][16:18]
            _mm = _arrayParameter[0][14:16]
            _aa = int(_arrayParameter[0][12:14])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][26:34])
            _hr = _arrayParameter[0][44:46]
            _mn = _arrayParameter[0][46:48]

            _dd = _arrayParameter[0][40:42]
            _mm = _arrayParameter[0][38:40]
            _aa = int(_arrayParameter[0][36:38])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][60:68])
            self._numberOfLastDebitNote = int(_arrayParameter[0][50:58])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][70:78])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][80:93])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][95:107])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][110:123])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][125:138])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][140:153])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][155:168])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][170:183])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][185:198])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][200:213])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][215:228])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][230:243])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][245:258])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][260:273])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][275:288])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][290:303])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][305:318])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][320:333])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][335:348])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][350:363])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][365:378])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][380:393])

            #self._persivSales = Util().DoValueDouble(_arrayParameter[0][501:519])
            #self._persivDebit = Util().DoValueDouble(_arrayParameter[0][521:539])
            #self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][541:559])
              
            #self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][561:579])
            #self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][581:599])
            #self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][601:619])
            #self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][621:639])
            #self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][641:659])
            #self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][661:679])
        except (ValueError):
          return

    if (len(trama) == 467): #(FLAG 63:01)
        try:
          _arrayParameter=str(trama).split(chr(0X0A))
          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][6:10])
            _hr = _arrayParameter[0][20:22]
            _mn = _arrayParameter[0][22:24]            
            _dd = _arrayParameter[0][16:18]
            _mm = _arrayParameter[0][14:16]
            _aa = int(_arrayParameter[0][12:14])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][26:34])
            _hr = _arrayParameter[0][44:46]
            _mn = _arrayParameter[0][46:48]

            _dd = _arrayParameter[0][40:42]
            _mm = _arrayParameter[0][38:40]
            _aa = int(_arrayParameter[0][36:38])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][60:68])
            self._numberOfLastDebitNote = int(_arrayParameter[0][50:58])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][70:78])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][80:98])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][100:118])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][120:138])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][140:158])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][160:178])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][180:198])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][200:218])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][220:238])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][240:258])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][260:278])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][280:298])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][300:318])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][320:338])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][340:358])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][360:378])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][380:398])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][400:418])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][420:438])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][440:458])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][460:478])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][480:498])

            #self._persivSales = Util().DoValueDouble(_arrayParameter[0][501:519])
            #self._persivDebit = Util().DoValueDouble(_arrayParameter[0][521:539])
            #self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][541:559])
              
            #self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][561:579])
            #self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][581:599])
            #self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][601:619])
            #self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][621:639])
            #self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][641:659])
            #self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][661:679])
        except (ValueError):
          return

    if (len(trama) == 419 or len(trama) == 533): #(FLAG 63:02 - 63:16 - 63:18)
        try:
          _arrayParameter=str(trama).split(chr(0X0A))
          if (len(_arrayParameter) > 0):
            self._numberOfLastZReport = int(_arrayParameter[0][6:10])
            _hr = _arrayParameter[0][20:22]
            _mn = _arrayParameter[0][22:24]            
            _dd = _arrayParameter[0][16:18]
            _mm = _arrayParameter[0][14:16]
            _aa = int(_arrayParameter[0][12:14])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._zReportDate = _Date
            self._zReportTime = _Time

            self._numberOfLastInvoice = int(_arrayParameter[0][26:34])
            _hr = _arrayParameter[0][44:46]
            _mn = _arrayParameter[0][46:48]

            _dd = _arrayParameter[0][40:42]
            _mm = _arrayParameter[0][38:40]
            _aa = int(_arrayParameter[0][36:38])+2000
            _Date = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
            _Time = str(_hr) +":"+ str(_mn) 
            self._lastInvoiceDate = _Date
            self._lastInvoiceTime = _Time

            self._numberOfLastCreditNote = int(_arrayParameter[0][60:68])
            self._numberOfLastDebitNote = int(_arrayParameter[0][50:58])            
            self._numberOfLastNonFiscal = int(_arrayParameter[0][70:78])
            self._freeSalesTax = Util().DoValueDouble(_arrayParameter[0][80:93])
            self._generalRate1Sale = Util().DoValueDouble(_arrayParameter[0][95:107])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[0][110:123])
            self._reducedRate2Sale = Util().DoValueDouble(_arrayParameter[0][125:138])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[0][140:153])
            self._additionalRate3Sal = Util().DoValueDouble(_arrayParameter[0][155:168])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[0][170:183])
            self._freeTaxDebit = Util().DoValueDouble(_arrayParameter[0][185:198])
            self._generalRateDebit = Util().DoValueDouble(_arrayParameter[0][200:213])
            self._generalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][215:228])
            self._reducedRateDebit = Util().DoValueDouble(_arrayParameter[0][230:243])
            self._reducedRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][245:258])
            self._additionalRateDebit = Util().DoValueDouble(_arrayParameter[0][260:273])
            self._additionalRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][275:288])
            self._freeTaxDevolution = Util().DoValueDouble(_arrayParameter[0][290:303])
            self._generalRateDevolution = Util().DoValueDouble(_arrayParameter[0][305:318])
            self._generalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][320:333])
            self._reducedRateDevolution = Util().DoValueDouble(_arrayParameter[0][335:348])
            self._reducedRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][350:363])
            self._additionalRateDevolution = Util().DoValueDouble(_arrayParameter[0][365:378])
            self._additionalRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][380:393])

            self._persivSales = Util().DoValueDouble(_arrayParameter[0][395:413])
            self._persivDebit = Util().DoValueDouble(_arrayParameter[0][415:433])
            self._persivDevolution = Util().DoValueDouble(_arrayParameter[0][435:453])
            
            #FLAG 63:16
            self._igtfRateSales = Util().DoValueDouble(_arrayParameter[0][455:473])
            self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[0][475:493])
            self._igtfRateDebit = Util().DoValueDouble(_arrayParameter[0][495:513])
            self._igtfRateTaxDebit = Util().DoValueDouble(_arrayParameter[0][515:533])
            self._igtfRateDevolution = Util().DoValueDouble(_arrayParameter[0][535:553])
            self._igtfRateTaxDevolution = Util().DoValueDouble(_arrayParameter[0][555:573])

            
        except (ValueError):
          return
class Util():
  def DoValueDouble(self, value):
      listItemsCount = len(value)
      integerValue=int(value[0:-2])
      floatingValue=value[(listItemsCount-2):]
      decimals=float(floatingValue)/100
      totalAmount= integerValue + decimals
      return totalAmount

class PrinterStatus(object):
    _printerErrorCode = 0
    _printerErrorDescription = ""
    _printerStatusCode = 0
    _printerStatusDescription = ""


    def __init__(self, trama):
        if(trama!=None):
            if (len(trama) == 10): # IMPRESORAS: HKA80 - SRP812 - PP9
                try:
                    _arrayParameter=str(trama[1:-1]).split(chr(0X0A))
                    self._setPrinterErrorCode(str(_arrayParameter[0][5:8]))          
                    self._setPrinterErrorDescription(str(_arrayParameter[0][10:12]) )  
                  
                except (ValueError):
                    return
                

    def PrinterErrorCode(self):
        return self._printerErrorCode

    def _setPrinterErrorCode(self, printerErrorCode):
        self._printerErrorCode = printerErrorCode

    def PrinterErrorDescription(self):
        return self._printerErrorDescription
    
    def _setPrinterErrorDescription(self, printerErrorDescription):
        self._printerErrorDescription = printerErrorDescription

#STATUS
    def PrinterStatusCode(self):
        return self._printerStatusCode

    def _setPrinterStatusCode(self, printerStatusCode):
        self._printerStatusCode = printerStatusCode

    def PrinterStatusDescription(self):
        return self._printerStatusDescription
    
    def _setPrinterStatusDescription(self, printerStatusDescription):
        self._printerStatusDescription = printerStatusDescription
class S1PrinterData(object):
  _cashierNumber = 0
  _totalDailySales = 0
  _lastInvoiceNumber = 0
  _quantityOfInvoicesToday = 0
  _lastDebtNoteNumber = 0
  _quantityDebtNoteToday = 0
  _lastNCNumber = 0
  _quantityOfNCToday = 0
  _numberNonFiscalDocuments = 0
  _quantityNonFiscalDocuments = 0
  _auditReportsCounter = 0
  _fiscalReportsCounter = 0
  _dailyClosureCounter = 0
  _rif = ""
  _registeredMachineNumber = ""
  _currentPrinterDate = "" #HORA
  _currentPrinterTime = "" #FECHA

  def __init__(self, trama):
    if(trama!=None):
      #print("longitud: "+ str(len(trama)))
      if (len(trama)>100): # and len(trama)<116): #116
        try:
          _arrayParameter=str(trama[1:-1]).split(chr(0X0A))
          #print ("estados S1 actual: " + str(_arrayParameter))
          self._setCashierNumber(_arrayParameter[0][3:5])          
          self._setTotalDailySales(Util().DoValueDouble(_arrayParameter[0][7:24]))        
          self._setLastInvoiceNumber(int(_arrayParameter[0][26:34]))           
          self._setQuantityOfInvoicesToday(int(_arrayParameter[0][36:41]))           
          self._setLastDebtNoteNumber(int(_arrayParameter[0][43:51]))            
          self._setQuantityDebtNoteToday(int(_arrayParameter[0][53:58]))
          self._setLastNCNumber(int(_arrayParameter[0][60:68]))
          self._setQuantityOfNCToday(int(_arrayParameter[0][70:75])) 
          self._setNumberNonFiscalDocuments(int(_arrayParameter[0][-71:-63]))
          self._setQuantityNonFiscalDocuments(int(_arrayParameter[0][-61:-56]))
          self._setFiscalReportsCounter(int(_arrayParameter[0][-54:-50]))                     
          self._setDailyClosureCounter(int(_arrayParameter[0][-48:-44]))
          self._setRif(str(_arrayParameter[0][-42:-31]))         
          self._setRegisteredMachineNumber(_arrayParameter[0][-29:-19])

          _hr = _arrayParameter[0][-17:-15]
          _mn = _arrayParameter[0][-15:-13]
          _sg = _arrayParameter[0][-13:-11]
          
          _dd = _arrayParameter[0][-9:-7]
          _mm = _arrayParameter[0][-7:-5]
          _aa = int(_arrayParameter[0][-5:-3])+2000

          _printerDate = str(_dd) + "-" + str(_mm) + "-" + str(_aa)
          _printerTime = str(_hr) +":"+ str(_mn) +":"+  str(_sg)
          self._setCurrentPrinterDate(_printerDate)
          self._setCurrentPrinterTime(_printerTime)
                
        except (ValueError):
          return

  def CashierNumber(self):
    return self._cashierNumber
  
  def _setCashierNumber(self, cashierNumber):
    self._cashierNumber = cashierNumber
    
  def TotalDailySales(self):
    return self._totalDailySales
  
  def _setTotalDailySales(self, totalDailySales):
    self._totalDailySales = totalDailySales
    
  def LastInvoiceNumber(self):
    return self._lastInvoiceNumber
  
  def _setLastInvoiceNumber(self, lastInvoiceNumber):
    self._lastInvoiceNumber = lastInvoiceNumber
  
  def QuantityOfInvoicesToday(self):
    return self._quantityOfInvoicesToday
  
  def _setQuantityOfInvoicesToday(self, quantityOfInvoicesToday):
    self._quantityOfInvoicesToday = quantityOfInvoicesToday
  
  def LastDebtNoteNumber(self):
    return self._lastDebtNoteNumber
  
  def _setLastDebtNoteNumber(self, lastDebtNoteNumber):
    self._lastDebtNoteNumber = lastDebtNoteNumber
  
  def QuantityDebtNoteToday(self):
    return self._quantityDebtNoteToday
  
  def _setQuantityDebtNoteToday(self, quantityDebtNoteToday):
    self._quantityDebtNoteToday = quantityDebtNoteToday
    
  def NumberNonFiscalDocuments(self):
    return self._numberNonFiscalDocuments
  
  def _setNumberNonFiscalDocuments(self, numberNonFiscalDocuments):
    self._numberNonFiscalDocuments = numberNonFiscalDocuments
    
  def QuantityNonFiscalDocuments(self):
    return self._quantityNonFiscalDocuments
  
  def _setQuantityNonFiscalDocuments(self, quantityNonFiscalDocuments):
    self._quantityNonFiscalDocuments = quantityNonFiscalDocuments
  
  def DailyClosureCounter(self):
    return self._dailyClosureCounter
  
  def _setDailyClosureCounter(self, dailyClosureCounter):
    self._dailyClosureCounter = dailyClosureCounter
  
  def AuditReportsCounter(self):
    return self._auditReportsCounter
  
  def _setAuditReportsCounter(self, auditReportsCounter):
    self._auditReportsCounter = auditReportsCounter

  def FiscalReportsCounter(self):
    return self._fiscalReportsCounter
  
  def _setFiscalReportsCounter(self, fiscalReportsCounter):
    self._fiscalReportsCounter = fiscalReportsCounter
  
  def Rif(self):
    return self._rif
  
  def _setRif(self, rif):
    self._rif = rif
  
  def RegisteredMachineNumber(self):
    return self._registeredMachineNumber
  
  def _setRegisteredMachineNumber(self, registeredMachineNumber):
    self._registeredMachineNumber= registeredMachineNumber

  def CurrentPrinterDate(self):
    return self._currentPrinterDate
  
  def _setCurrentPrinterDate(self, currentPrinterDate):
    self._currentPrinterDate = currentPrinterDate

  def CurrentPrinterTime(self):
    return self._currentPrinterTime
  
  def _setCurrentPrinterTime(self, currentPrinterTime):
    self._currentPrinterTime = currentPrinterTime
 
  def LastNCNumber(self):
    return self._lastNCNumber
  
  def _setLastNCNumber(self, lastNCNumber):
    self._lastNCNumber = lastNCNumber
  
  def QuantityOfNCToday(self):
    return self._quantityOfNCToday
  
  def _setQuantityOfNCToday (self, quantityOfNCToday):
    self._quantityOfNCToday = quantityOfNCToday
class S2PrinterData(object):
  _subTotalBases = 0
  _subTotalTax = 0
  _dataDummy = 0
  _amountPayable = 0
  _numberPaymentsMade = 0
  _typeDocument = 0
  _quantityArticles = 0
  _condition = 0

  def __init__(self, trama):
    if (trama != None):
      if (len(trama) == 84): #longitud de la trama SRP350 
        try:
          
          _arrayParameter = str(trama[1:-1]).split(chr(0X0A))
          self._setSubTotalBases(Util().DoValueDouble(_arrayParameter[0][4:17]))
          self._setSubTotalTax(Util().DoValueDouble(_arrayParameter[0][20:33]))
          self._setDataDummy(Util().DoValueDouble(_arrayParameter[0][36:49]))
          self._setQuantityArticles(int(_arrayParameter[0][51:64]))
          self._setAmountPayable(Util().DoValueDouble(_arrayParameter[0][-25:-12]))
          self._setNumberPaymentsMade(int(_arrayParameter[0][-10:-6]))
          self._setTypeDocument(int(_arrayParameter[0][-4]))
        except (ValueError):
          return
      if (len(trama) == 104): #longitud de la trama HKA80 FLAG 63:01 - 63:03 - 63:17 - 63:19 
      
            
            _arrayParameter = str(trama[1:-1]).split(chr(0X0A))
            self._setSubTotalBases(Util().DoValueDouble(_arrayParameter[0][4:21]))
            self._setSubTotalTax(Util().DoValueDouble(_arrayParameter[0][24:41]))
            self._setDataDummy(Util().DoValueDouble(_arrayParameter[0][44:61]))
            self._setQuantityArticles(int(_arrayParameter[0][63:80]))
            self._setAmountPayable(Util().DoValueDouble(_arrayParameter[0][-29:-12]))
            self._setNumberPaymentsMade(int(_arrayParameter[0][-10:-6]))
            self._setTypeDocument(int(_arrayParameter[0][-4]))

      if (len(trama) == 77): #longitud de la trama HKA80 FLAG 63:00 - 63:02 - 63:16 - 63:18 
      
            
            _arrayParameter = str(trama[1:-1]).split(chr(0X0A))
            self._setSubTotalBases(Util().DoValueDouble(_arrayParameter[0][4:17]))
            self._setSubTotalTax(Util().DoValueDouble(_arrayParameter[0][20:33]))
            self._setDataDummy(Util().DoValueDouble(_arrayParameter[0][36:49]))
            self._setQuantityArticles(int(_arrayParameter[0][51:57]))
            self._setAmountPayable(Util().DoValueDouble(_arrayParameter[0][-25:-12]))
            self._setNumberPaymentsMade(int(_arrayParameter[0][-10:-6]))
            self._setTypeDocument(int(_arrayParameter[0][-4]))
  
  
  def SubTotalBases(self):
    return self._subTotalBases
  
  def SubTotalTax(self):
    return self._subTotalTax
  
  def DataDummy(self):
    return self._dataDummy
  
  def AmountPayable(self):
    return self._amountPayable
  
  def NumberPaymentsMade(self):
    return self._numberPaymentsMade
  
  def QuantityArticles(self):
    return self._quantityArticles
  
  def TypeDocument(self):
    return self._typeDocument
  
  def Condition(self):
    return self._condition
  
  def _setQuantityArticles(self, value):
    self._quantityArticles = value
    
  def _setTypeDocument(self, type):
    self._typeDocument = type
    
  def _setCondition(self, condition):
    self._condition = condition
  
  def _setSubTotalBases(self, subTotalBases):
    self._subTotalBases = subTotalBases
    
  def _setSubTotalTax(self, subTotalTax):
    self._subTotalTax = subTotalTax
    
  def _setDataDummy(self, dataDummy):
    self._dataDummy = dataDummy

  def _setAmountPayable(self, amountPayable):
    self._amountPayable = amountPayable

  def _setNumberPaymentsMade(self, numberPaymentsMade):
    self._numberPaymentsMade = numberPaymentsMade
class S3PrinterData(object):
  _typeTax1=0
  _tax1=0
  _typeTax2=0
  _tax2=0
  _typeTax3=0
  _tax3=0
  _igtf=0
  _typeIgtf=0
  _systemFlags=[]
  
  def __init__(self, trama):
    if (trama != None):
      if (len(trama) == 150): #TRAMA CON FLGAS 63-01,02,03
        try:
          _arrayParameter=str(trama[1:-1]).split(chr(0X0A))#(0X0A))
          
 
          self._setTypeTax1(_arrayParameter[0][3])            
          self._setTax1(Util().DoValueDouble(_arrayParameter[0][4:8]))          
          self._setTypeTax2(_arrayParameter[0][10])          
          self._setTax2(Util().DoValueDouble(_arrayParameter[0][11:15]))         
          self._setTypeTax3(_arrayParameter[0][17])          
          self._setTax3(Util().DoValueDouble(_arrayParameter[0][18:22]))
          
          _flagsQuantity = int(len(_arrayParameter[0][24:152]) / 2)
          self._systemFlags = []
          _index = 0
          _iteration = 0
          while (_iteration < _flagsQuantity):
            self._systemFlags.append(str(_arrayParameter[0][24:152][_index: _index+2])) #_index, 2 #[_iteration]
            _index = _index + 2
            _iteration+=1
          self._setSystemFlags(self._systemFlags)
        except (ValueError):
          return
    if (len(trama) == 156): #TRAMA CON FLAGS 63-16,17,18,19
        try:
          _arrayParameter=str(trama[1:-1]).split(chr(0X0A))#(0X0A))
          
 
          self._setTypeTax1(_arrayParameter[0][3])            
          self._setTax1(Util().DoValueDouble(_arrayParameter[0][4:8]))          
          self._setTypeTax2(_arrayParameter[0][10])          
          self._setTax2(Util().DoValueDouble(_arrayParameter[0][11:15]))         
          self._setTypeTax3(_arrayParameter[0][17])          
          self._setTax3(Util().DoValueDouble(_arrayParameter[0][18:22]))
          self._setTypeIgtf(_arrayParameter[0][24])          
          self._setIgtf(Util().DoValueDouble(_arrayParameter[0][26:29]))
          
          _flagsQuantity = int(len(_arrayParameter[0][30:159]) / 2)
          self._systemFlags = []
          _index = 0
          _iteration = 0
          while (_iteration < _flagsQuantity):
            self._systemFlags.append(str(_arrayParameter[0][31:159][_index: _index+2])) #_index, 2 #[_iteration]
           
            _index = _index + 2
            _iteration+=1
          
          self._setSystemFlags(self._systemFlags)
        except (ValueError):
          return

  def TypeTax1(self):
    return self._typeTax1
  
  def Tax1(self):
    return self._tax1
  
  def TypeTax2(self):
    return self._typeTax2
  
  def Tax2(self):
    return self._tax2
  
  def TypeTax3(self):
    return self._typeTax3
  
  def Tax3(self):
    return self._tax3

  def Igtf(self):
    return self._igtf
  
  def TypeIgtf(self):
    return self._typeIgtf
  
  def AllSystemFlags(self):
    return self._systemFlags
  
  def _setTypeTax1(self, typeTax1):
    self._typeTax1 = typeTax1
  
  def _setTax1(self, tax1):
    self._tax1 = tax1
    
  def _setTypeTax2(self, typeTax2):
    self._typeTax2 = typeTax2
    
  def _setTax2(self, tax2):
    self._tax2 = tax2
    
  def _setTypeTax3(self, typeTax3):
    self._typeTax3 = typeTax3
    
  def _setTax3(self, tax3):
    self._tax3 = tax3
  
  def _setIgtf(self, igtf):
    self._igtf = igtf
  
  def _setTypeIgtf(self, typeIgtf):
      self._typeIgtf = typeIgtf
    
  def _setSystemFlags(self, pSystemFlags): #[]
    self._systemFlags = pSystemFlags
class S4PrinterData(object):
  
  def __init__(self, trama):
    if (trama != None):
      if (len(trama) == 459): # FLAG 63:19 - 63:01 - 63:03 - 63:17
        self._allMeansOfPayment = ""
        try:
          _arrayParameter=str(trama[1:-1]).split(chr(0X0A))
          _numberOfMeansOfPayment = len(_arrayParameter)
          _iteration = 0
          _valor = 0
          while (_iteration < _numberOfMeansOfPayment):
            _cadena = _arrayParameter[_iteration]
            if (_iteration < 0):
              _valor = str(_cadena[2:])
            else:
              _valor = _cadena
            self._allMeansOfPayment += "\nMedio de Pago " + str(_iteration+1) + " : "  + str(Util().DoValueDouble(_valor[3:21]))
            self._allMeansOfPayment += "\nMedio de Pago 2 "" : "  + str(Util().DoValueDouble(_valor[23:41]))
            self._allMeansOfPayment += "\nMedio de Pago 3 "" : "  + str(Util().DoValueDouble(_valor[43:61]))
            self._allMeansOfPayment += "\nMedio de Pago 4 "" : "  + str(Util().DoValueDouble(_valor[63:81]))
            self._allMeansOfPayment += "\nMedio de Pago 5 "" : "  + str(Util().DoValueDouble(_valor[83:101]))
            self._allMeansOfPayment += "\nMedio de Pago 6 "" : "  + str(Util().DoValueDouble(_valor[103:121]))
            self._allMeansOfPayment += "\nMedio de Pago 7 "" : "  + str(Util().DoValueDouble(_valor[123:141]))
            self._allMeansOfPayment += "\nMedio de Pago 8 "" : "  + str(Util().DoValueDouble(_valor[143:161]))
            self._allMeansOfPayment += "\nMedio de Pago 9 "" : "  + str(Util().DoValueDouble(_valor[163:181]))
            self._allMeansOfPayment += "\nMedio de Pago 10 "" : "  + str(Util().DoValueDouble(_valor[183:201]))
            self._allMeansOfPayment += "\nMedio de Pago 11 "" : "  + str(Util().DoValueDouble(_valor[203:221]))
            self._allMeansOfPayment += "\nMedio de Pago 12 "" : "  + str(Util().DoValueDouble(_valor[223:241]))
            self._allMeansOfPayment += "\nMedio de Pago 13 "" : "  + str(Util().DoValueDouble(_valor[243:261]))
            self._allMeansOfPayment += "\nMedio de Pago 14 "" : "  + str(Util().DoValueDouble(_valor[263:281]))
            self._allMeansOfPayment += "\nMedio de Pago 15 "" : "  + str(Util().DoValueDouble(_valor[283:301]))
            self._allMeansOfPayment += "\nMedio de Pago 16 "" : "  + str(Util().DoValueDouble(_valor[303:321]))
            self._allMeansOfPayment += "\nMedio de Pago 17 "" : "  + str(Util().DoValueDouble(_valor[323:341]))
            self._allMeansOfPayment += "\nMedio de Pago 18 "" : "  + str(Util().DoValueDouble(_valor[343:361]))
            self._allMeansOfPayment += "\nMedio de Pago 19 "" : "  + str(Util().DoValueDouble(_valor[363:381]))
            self._allMeansOfPayment += "\nMedio de Pago 20 "" : "  + str(Util().DoValueDouble(_valor[383:401]))
            self._allMeansOfPayment += "\nMedio de Pago 21 "" : "  + str(Util().DoValueDouble(_valor[403:421]))
            self._allMeansOfPayment += "\nMedio de Pago 22 "" : "  + str(Util().DoValueDouble(_valor[423:441]))
            self._allMeansOfPayment += "\nMedio de Pago 23 "" : "  + str(Util().DoValueDouble(_valor[443:461]))
            self._allMeansOfPayment += "\nMedio de Pago 24 "" : "  + str(Util().DoValueDouble(_valor[463:481]))
            _iteration+=1
          self._setAllMeansOfPayment(self._allMeansOfPayment)
        except (ValueError):
          return

    if (len(trama) == 339): # FLAG 63:00 - 63:02 - 63:16 - 63:18
          self._allMeansOfPayment = ""
          try:
            _arrayParameter=str(trama[1:-1]).split(chr(0X0A))
            _numberOfMeansOfPayment = len(_arrayParameter)
            _iteration = 0
            _valor = 0
            while (_iteration < _numberOfMeansOfPayment):
              _cadena = _arrayParameter[_iteration]
              if (_iteration < 0):
                _valor = str(_cadena[2:])
              else:
                _valor = _cadena
              self._allMeansOfPayment += "\nMedio de Pago " + str(_iteration+1) + " : "  + str(Util().DoValueDouble(_valor[3:16]))
              self._allMeansOfPayment += "\nMedio de Pago 2 "" : "  + str(Util().DoValueDouble(_valor[18:31]))
              self._allMeansOfPayment += "\nMedio de Pago 3 "" : "  + str(Util().DoValueDouble(_valor[33:46]))
              self._allMeansOfPayment += "\nMedio de Pago 4 "" : "  + str(Util().DoValueDouble(_valor[48:61]))
              self._allMeansOfPayment += "\nMedio de Pago 5 "" : "  + str(Util().DoValueDouble(_valor[63:76]))
              self._allMeansOfPayment += "\nMedio de Pago 6 "" : "  + str(Util().DoValueDouble(_valor[78:91]))
              self._allMeansOfPayment += "\nMedio de Pago 7 "" : "  + str(Util().DoValueDouble(_valor[93:106]))
              self._allMeansOfPayment += "\nMedio de Pago 8 "" : "  + str(Util().DoValueDouble(_valor[108:121]))
              self._allMeansOfPayment += "\nMedio de Pago 9 "" : "  + str(Util().DoValueDouble(_valor[123:136]))
              self._allMeansOfPayment += "\nMedio de Pago 10 "" : "  + str(Util().DoValueDouble(_valor[138:151]))
              self._allMeansOfPayment += "\nMedio de Pago 11 "" : "  + str(Util().DoValueDouble(_valor[153:166]))
              self._allMeansOfPayment += "\nMedio de Pago 12 "" : "  + str(Util().DoValueDouble(_valor[168:181]))
              self._allMeansOfPayment += "\nMedio de Pago 13 "" : "  + str(Util().DoValueDouble(_valor[183:196]))
              self._allMeansOfPayment += "\nMedio de Pago 14 "" : "  + str(Util().DoValueDouble(_valor[198:211]))
              self._allMeansOfPayment += "\nMedio de Pago 15 "" : "  + str(Util().DoValueDouble(_valor[213:226]))
              self._allMeansOfPayment += "\nMedio de Pago 16 "" : "  + str(Util().DoValueDouble(_valor[228:241]))
              self._allMeansOfPayment += "\nMedio de Pago 17 "" : "  + str(Util().DoValueDouble(_valor[243:256]))
              self._allMeansOfPayment += "\nMedio de Pago 18 "" : "  + str(Util().DoValueDouble(_valor[258:271]))
              self._allMeansOfPayment += "\nMedio de Pago 19 "" : "  + str(Util().DoValueDouble(_valor[273:286]))
              self._allMeansOfPayment += "\nMedio de Pago 20 "" : "  + str(Util().DoValueDouble(_valor[288:301]))
              self._allMeansOfPayment += "\nMedio de Pago 21 "" : "  + str(Util().DoValueDouble(_valor[303:316]))
              self._allMeansOfPayment += "\nMedio de Pago 22 "" : "  + str(Util().DoValueDouble(_valor[318:331]))
              self._allMeansOfPayment += "\nMedio de Pago 23 "" : "  + str(Util().DoValueDouble(_valor[333:346]))
              self._allMeansOfPayment += "\nMedio de Pago 24 "" : "  + str(Util().DoValueDouble(_valor[348:361]))
              _iteration+=1
            self._setAllMeansOfPayment(self._allMeansOfPayment)
          except (ValueError):
            return

  def AllMeansOfPayment(self):
    return self._allMeansOfPayment

  def _setAllMeansOfPayment(self, pAllMeansOfPayment):
    self._allMeansOfPayment = pAllMeansOfPayment
class S5PrinterData(object):
  _rif=""
  _registeredMachineNumber=""
  _auditMemoryNumber=0
  _auditMemoryTotalCapacity=0
  _auditMemoryFreeCapacity=0
  _numberRegisteredDocuments=0
  
  def __init__(self, trama):
    if (trama != None):
        if (len(trama) > 0):
          try:
            _arrayParameter=str(trama[1:-1]).split(chr(0X0A))
            if (len(_arrayParameter) >= 0):
                self._setRIF(_arrayParameter[0][3:14])
                self._setRegisteredMachineNumber(_arrayParameter[0][16:26])
                self._setNumberMemoryAudit(int(_arrayParameter[0][28:32]))
                self._setCapacityTotalMemoryAudit(int(_arrayParameter[0][34:38]))
                self._setAuditMemoryFreeCapacity(int(_arrayParameter[0][40:44]))
                self._setNumberDocumentRegisters(int(_arrayParameter[0][46:52]))
          except (ValueError):
              return
  
  def RIF(self):
    return self._rif

  def RegisteredMachineNumber(self):
    return self._registeredMachineNumber

  def AuditMemoryNumber(self):
    return self._auditMemoryNumber

  def AuditMemoryTotalCapacity(self):
    return self._auditMemoryTotalCapacity

  def AuditMemoryFreeCapacity(self):
    return self._auditMemoryFreeCapacity

  def NumberRegisteredDocuments(self):
    return self._numberRegisteredDocuments

  def _setRIF(self, RIF):
    self._rif = RIF

  def _setRegisteredMachineNumber(self, registeredMachineNumber):
    self._registeredMachineNumber = registeredMachineNumber

  def _setNumberMemoryAudit(self, numberMemoryAudit):
    self._auditMemoryNumber = numberMemoryAudit

  def _setCapacityTotalMemoryAudit(self, capacityTotalMemoryAudit):
    self._auditMemoryTotalCapacity = capacityTotalMemoryAudit

  def _setAuditMemoryFreeCapacity(self, pAuditMemoryFreeCapacity):
    self._auditMemoryFreeCapacity = pAuditMemoryFreeCapacity

  def _setNumberDocumentRegisters(self, numberDocumentRegisters):
    self._numberRegisteredDocuments = numberDocumentRegisters
class S6PrinterData(object):
  _bit_Facturacion=""
  _bit_Slip=""
  _bit_Validacion=""
  
  def __init__(self, trama):
    if (trama != None):
      if (len(trama) > 0):
        _arrayParameter=str(trama[1:-1]).split(chr(0X0A))
        if (len(_arrayParameter) >= 0):
          try:
            self._setBit_Facturacion(str(_arrayParameter[0][2:]))
            self._setBit_Slip(_arrayParameter[1])
            self._setBit_Validacion(_arrayParameter[2])
          except (ValueError):
            return
  
  def Bit_Facturacion(self):
    return self._bit_Facturacion
  
  def Bit_Slip(self):
    return self._bit_Slip
  
  def Bit_Validacion(self):
    return self._bit_Validacion
  
  def _setBit_Facturacion(self, bitFacturacion):
    self._bit_Facturacion = bitFacturacion
    
  def _setBit_Slip(self, bitSlip):
    self._bit_Slip = bitSlip
    
  def _setBit_Validacion(self, bitValidacion):
    self._bit_Validacion = bitValidacion
class S7PrinterData(object):
  _micr=""
  
  def __init__(self, trama):
    if (trama != None):
      if (len(trama) > 0):
          try:
            _arrayParameter=str(trama[1:-2]).split(chr(0X0A))#(0X0A))
            if (len(_arrayParameter) >= 1):
              self._setMICR(str(_arrayParameter[0][2:]))
          except (ValueError):
              return
  
  def MICR(self):
    return self._micr
  
  def _setMICR(self, micr):
    self._micr = micr
class S8EPrinterData(object):
  _encabezado1=""
  _encabezado2=""
  _encabezado3=""
  _encabezado4=""
  _encabezado5=""
  _encabezado6=""
  _encabezado7=""
  _encabezado8=""
  
  def __init__(self, trama):
    if (trama != None):
      _header = trama.split('\n')
      if (len(_header) > 0):
        self._setEncabezado1(_header[0][3:])
        self._setEncabezado2(_header[1])
        self._setEncabezado3(_header[2])
        self._setEncabezado4(_header[3])
        self._setEncabezado5(_header[4])
        self._setEncabezado6(_header[5])
        self._setEncabezado7(_header[6])
        self._setEncabezado8(_header[7][:-2])
  
  def Header1(self):
    return self._encabezado1
  
  def Header2(self):
    return self._encabezado2
  
  def Header3(self):
    return self._encabezado3
  
  def Header4(self):
    return self._encabezado4
  
  def Header5(self):
    return self._encabezado5
  
  def Header6(self):
    return self._encabezado6
  
  def Header7(self):
    return self._encabezado7
  
  def Header8(self):
    return self._encabezado8
  
  def _setEncabezado1(self, Encabezado1):
    self._encabezado1 = Encabezado1
  
  def _setEncabezado2(self, Encabezado2):
    self._encabezado2 = Encabezado2
  
  def _setEncabezado3(self, Encabezado3):
    self._encabezado3 = Encabezado3

  def _setEncabezado4(self, Encabezado4):
    self._encabezado4 = Encabezado4
  
  def _setEncabezado5(self, Encabezado5):
    self._encabezado5 = Encabezado5

  def _setEncabezado6(self, Encabezado6):
    self._encabezado6 = Encabezado6

  def _setEncabezado7(self, Encabezado7):
    self._encabezado7 = Encabezado7

  def _setEncabezado8(self, Encabezado8):
    self._encabezado8 = Encabezado8
class S8PPrinterData(object):
  _piedeTicket1=""
  _piedeTicket2=""
  _piedeTicket3=""
  _piedeTicket4=""
  _piedeTicket5=""
  _piedeTicket6=""
  _piedeTicket7=""
  _piedeTicket8=""
  
  def __init__(self, trama):
    if (trama != None):
      _footer = trama.split('\n')
      if (len(_footer) > 0):
        self._setPiedeTicket1(_footer[0][4:])
        self._setPiedeTicket2(_footer[1])
        self._setPiedeTicket3(_footer[2])
        self._setPiedeTicket4(_footer[3])
        self._setPiedeTicket5(_footer[4])
        self._setPiedeTicket6(_footer[5])
        self._setPiedeTicket7(_footer[6])
        self._setPiedeTicket8(_footer[7][:-2])
  
  def Footer1(self):
    return self._piedeTicket1
  
  def Footer2(self):
    return self._piedeTicket2
  
  def Footer3(self):
    return self._piedeTicket3
  
  def Footer4(self):
    return self._piedeTicket4
  
  def Footer5(self):
    return self._piedeTicket5
  
  def Footer6(self):
    return self._piedeTicket6
  
  def Footer7(self):
    return self._piedeTicket7
  
  def Footer8(self):
    return self._piedeTicket8
  
  def _setPiedeTicket1(self, PiedeTicket1):
    self._piedeTicket1 = PiedeTicket1
  
  def _setPiedeTicket2(self, PiedeTicket2):
    self._piedeTicket2 = PiedeTicket2
  
  def _setPiedeTicket3(self, PiedeTicket3):
    self._piedeTicket3 = PiedeTicket3
  
  def _setPiedeTicket4(self, PiedeTicket4):
    self._piedeTicket4 = PiedeTicket4
  
  def _setPiedeTicket5(self, PiedeTicket5):
    self._piedeTicket5 = PiedeTicket5
  
  def _setPiedeTicket6(self, PiedeTicket6):
    self._piedeTicket6 = PiedeTicket6
  
  def _setPiedeTicket7(self, PiedeTicket7):
    self._piedeTicket7 = PiedeTicket7
  
  def _setPiedeTicket8(self, PiedeTicket8):
    self._piedeTicket8 = PiedeTicket8
class SVPrinterData(object):
    _pmodel = ""
    _pcountry = ""


    def __init__(self, trama):
        if(trama!=None):
            #print("longitud: "+ str(len(trama)))
            if (len(trama) == 10): # IMPRESORAS: HKA80 - SRP812 - PP9
                try:
                    _arrayParameter=str(trama[1:-1]).split(chr(0X0A))
                    #print ("estados SV actual: " + str(_arrayParameter))
                    self._setPmodel(str(_arrayParameter[0][5:8]))          
                    self._setPcountry(str(_arrayParameter[0][10:12]) )  
                  
                except (ValueError):
                    return
                

    def Pmodel(self):
        return self._pmodel

    def _setPmodel(self, pmodel):
        self._pmodel = pmodel

    def Pcountry(self):
        return self._pcountry
    
    def _setPcountry(self, pcountry):
        self._pcountry = pcountry
class AcumuladosX(object):
  #Global variables
  _freeTax = 0
  _generalRate1 = 0
  _generalRate1Tax = 0
  _reducedRate2 = 0
  _reducedRate2Tax = 0
  _additionalRate3 = 0
  _additionalRate3Tax = 0
  _igtfRateSales = 0
  _igtfRateTaxSales = 0

  def __init__(self, trama):
    if (trama != None):
      if (len(trama) > 0):
        try:
          _arrayParameter = trama.split(chr(0X0A)) 
          if (len(_arrayParameter) >= 7):
            self._freeTax = Util().DoValueDouble(_arrayParameter[0])
            self._generalRate1 = Util().DoValueDouble(_arrayParameter[1])
            self._reducedRate2 = Util().DoValueDouble(_arrayParameter[2])
            self._additionalRate3 = Util().DoValueDouble(_arrayParameter[3])
            self._generalRate1Tax = Util().DoValueDouble(_arrayParameter[4])
            self._reducedRate2Tax = Util().DoValueDouble(_arrayParameter[5])
            self._additionalRate3Tax = Util().DoValueDouble(_arrayParameter[6])
            self._igtfRateSales = Util().DoValueDouble(_arrayParameter[7])
            self._igtfRateTaxSales = Util().DoValueDouble(_arrayParameter[8])
        except(ValueError):
            return
  
  def FreeTax(self):
    return self._freeTax
  
  def GeneralRate1(self):
    return self._generalRate1
  
  def GeneralRate1Tax(self):
    return self._generalRate1Tax
  
  def ReducedRate2(self):
    return self._reducedRate2

  def ReducedRate2Tax(self):
    return self._reducedRate2Tax
  
  def AdditionalRate3(self):
    return self._additionalRate3
    
  def AdditionalRate3Tax(self):
    return self._additionalRate3Tax

  def IgtfRateSales(self):
    return self._igtfRateSales

  def IgtfRateTaxSales(self):
    return self._igtfRateTaxSales
