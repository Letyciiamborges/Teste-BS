#Bom Sucesso
from asyncio import sleep
from ctypes import*
from ctypes.wintypes import INT
from lib2to3.pytree import convert
from pickletools import uint2
from platform import java_ver
from sqlite3 import Cursor
import string
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pyModbusTCP.client import ModbusClient as ModbusTCPClient
from ctypes import BigEndianStructure, LittleEndianStructure
import struct
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient
#-------------------
from mysql.connector.errors import Error
from datetime import datetime
import time
import gc
#conversão de número(TCP)
import numpy as np
from pyModbusTCP.client import ModbusClient as ModbusTCPClient
from ctypes import BigEndianStructure, LittleEndianStructure
#import serial
import mysql.connector
from mysql.connector import Error
from subprocess import Popen, STDOUT,PIPE,call
#from SaveData import*
#from alarmeInversor import*
import envioHTTPEDT
import envioHTTPinversores
import socket
# Para meu codigo
from pyModbusTCP.client import ModbusClient
import time

# Informações dos inversores 
SERVER_HOST3 = "192.168.3.103"
SERVER_HOST4 = "192.168.3.104"
SERVER_HOST5 = "192.168.3.105"

SERVER_PORT3 = 502
SERVER_PORT4 = 502
SERVER_PORT5 = 502

c3 = ModbusClient()
c4 = ModbusClient()
c5 = ModbusClient()

c3.host(SERVER_HOST3)
c4.host(SERVER_HOST4)
c5.host(SERVER_HOST5)

c3.port(SERVER_PORT3)
c4.port(SERVER_PORT4)
c5.port(SERVER_PORT5)

#----------------------------------

def conectar_internet():
    nome = 'SOLAR GRID'
    manipulador = Popen('netsh wlan connect {}'.format(nome),shell=True, stdout=PIPE, stderr = STDOUT, stdin =PIPE)
    sleep(2)
    manipulador.stdin.write(b'SolarGrid43')
    while manipulador.poll()== None:
        print(manipulador.stdout.readline().strip())
    try:
        if call('ping -n 1 www.google.com')==0:
            print('conectado')
            return 1
    except:
        print("falha")
        return 0
def checkConnection():
    try:
        banco = mysql.connector.connect(host ="212.1.208.151", user="u874852425_mvpower",passwd="6nt#EeoN", database="u874852425_dadosmvp")
    except Error as erro:
        print("Falha na comunicacao: ")
    finally:
        try:
            if(banco.is_connected()):
                banco.close()
                print("Conexao finalizadada")
                return 1       
        except Exception:
            print("nao conectou no DB")
            return 0

# Para pegar os registros ??? olhar               
def run_sync_dados(id,porta, register_ini, register_fim):
    client = ModbusClient(method='rtu', port=porta, timeout=0.25, baudrate=9600)
    client.strict=False
    client.connect()
    try:
        dados = client.read_input_registers(register_ini,register_fim,unit=id)
    except Exception as e:
        print('Erro')
    try:
        a = dados.registers
    except Exception as e:
        return []
    client.close()
    return a
''''
#conexão TCP
'''


def main():
    energia = 0
    vetorInversores ={}


    while True:
        eDiariaTotal=0
        cont=0
        valor=str(datetime.now())
        print(valor)
        print(valor[11],valor[12],valor[13],valor[14],valor[15])
        t2=int(valor[17]+valor[18])
        tempo =int(valor[14]+valor[15])%10
        tempo2 = int(valor[15])%5
        
        #intervalo de 5min entre envios
        if(tempo2!=0): 
            print('tempo', tempo)
            print(t2)
            print(((5-tempo2)*60)-t2)
            time.sleep(((5-tempo2)*60)-t2)
            
        data = str(datetime.now())
        lista = list(data)
        lista[17]='0'
        lista[18]='0'
        data="".join(lista)
        print(data)



        # Dados dos registros do inversor
        # colocar inversores aqui
        for i in range (0,3):
            if not c3.is_open():
                if not c3.open():
                    print("unable to connect to "+SERVER_HOST3+":"+str(SERVER_PORT3))
            if c3.is_open():
                regs3 = c3.read_holding_registers(40070, 50)
            if regs3:
                print("inversor 3")
                vetorinv3=[float(regs3[33]), float(regs3[31]), float(regs3[10]), float(regs3[11]), float(regs3[12]), float(regs3[3]), float(regs3[4]), float(regs3[5]), float(regs3[14]), float(regs3[21]), float(regs3[16]), float(regs3[38])]
                eDiariaTotal+= (float(regs3[14]/1000))
                print(vetorinv3)
                #print("energia", eDiariaTotal)
                print("Alarme: ", 0)
                print("status: ", float(regs3[38]))

            if not c4.is_open():
                if not c4.open():
                    print("unable to connect to "+SERVER_HOST4+":"+str(SERVER_PORT4))
            if c4.is_open():
                regs4 = c4.read_holding_registers(40070, 50)
            if regs4:
                print("inversor 4")
                vetorinv4=[float(regs4[33]), float(regs4[31]), float(regs4[10]), float(regs4[11]), float(regs4[12]), float(regs4[3]), float(regs4[4]), float(regs4[5]), float(regs4[14]), float(regs4[21]), float(regs4[16]), float(regs4[38])]
                eDiariaTotal+= (float(regs4[14]/1000))
                print(vetorinv4)
                #print("energia", eDiariaTotal)
                print("Alarme: ", 0)
                print("status: ", float(regs3[38]))

            if not c5.is_open():
                if not c5.open():
                    print("unable to connect to "+SERVER_HOST5+":"+str(SERVER_PORT5))
            if c5.is_open():
                regs5 = c5.read_holding_registers(40070, 50)
            if regs5:
                print("inversor 5")
                vetorinv5=[float(regs5[33]), float(regs5[31]), float(regs5[10]), float(regs5[11]), float(regs5[12]), float(regs5[3]), float(regs5[4]), float(regs5[5]), float(regs5[14]), float(regs5[21]), float(regs5[16]), float(regs5[38])]
                eDiariaTotal+= (float(regs5[14]/1000))
                print(vetorinv5)
                #print("energia", eDiariaTotal)
                print("Alarme: ", 0)
                print("status: ", float(regs5[38]))

    #------------------------VERIFICAR A CONEXAO----------------------------------------
        vetorInversores.update(regs3)
        vetorInversores.update( regs4)
        vetorInversores.update(regs5)

        vetor_energia={}
        energia_vetor=[]
        energia_vetor=[eDiariaTotal]
        vetor_energia[1] = energia_vetor
        
        inversor =  JsonManager(vetorInversores,data,1,3)
        energia = JsonManager(vetor_energia,data,1,2)
        variavel= 0
        if(checkConnection() ==1):
            if(len(inversor.read_json('data/inversor.json'))==0 and len(energia.read_json('data/energia.json'))==0):
                print("Arquivos vazios e conectado a internet")
                #mysQL_envio(vetorInversores,vetorCombiners,eDiariaTotal*100,data)
                envioHTTPinversores.envio_Inversores(vetorInversores)
                envioHTTPEDT.envio_EDT(eDiariaTotal*100)
            else:
                vetor ={}
                print("Arquivos cheios")
                for i in range(0, len(inversor.read_json('data/inversor.json'))):
                    vetor = inversor.read_json('data/inversor.json')[i]
                    print(vetor)
                    inversor.envio_inversor(vetor,i)
                    
                    vetor = {}
                
                for i in range(0,len(energia.read_json('data/energia.json'))):
                    vetor = energia.read_json('data/energia.json')[i]['1']
                    hora= vetor[1]
                    print('energia',vetor)
                    #mysQl_energiaDiaria(vetor[0],hora)
                    #envioHTTPEDT.envio_EDT(energiaTotal*100,data)
                    energia.envio_EDT(vetor)
                    vetor = {}

                #ENVIOS REALIZADOS -> LIMPAR ARQUIVOS    
                inversor.clear('data/inversor.json')
                energia.clear('data/energia.json')             
        else:
            print("SEM INTERNET")
            #inversor.create_json('data/inversor.json')
            #combiner.create_json('data/combiner.json')
            #esta.create_json('data/estacao.json')
            #energia.create_json('data/energia.json')
            inversor.update_json('data/inversor.json')
            energia.update_json('data/energia.json')  

#----------------------------------------------------------------
    time.sleep(2)
        
        
#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
