#Envio
from argparse import _VersionAction
from dataclasses import dataclass
import aiohttp
import asyncio
import json


#
# Função para envio dos dados em HTTP (request.post)
#
async def envioPost(dadosMain,url,head):
    async with aiohttp.ClientSession(headers=head) as session:
        print(url)
        for dado in dadosMain:
            async with session.post(url,json=dado) as resp:
                print("Codigo de resposta: <",resp.status,">")
                





def envio_Inversores(vetor,vetor2):
    #
    # Informações fundamentais para a comunicação com o servidor (token url e cabeçalho)
    #
    myToken = 'NKick68KLONcwzcRMS3KZyI7m4g5xoJwvDcsmS46JDhECTmFaSuhr0ew53yRW5t8f8wIjdpfScR8tRcjEWa8gXiDhVwtAsk9r0Q9oYRjyWoYP9VnMxUvPQnY'
    myUrl = 'https://api-data-receiver.mv-toth.com/inversors'
    head = {'X-API-KEY':myToken}
    print("Preparando envio de inversores")
    a=9
    listaDados = [None] * 2

    #
    # Definir a lista de dados
    #

    for i in range (101,103):
        if(vetor.get(i-100)!=None and len(vetor[i-100])==76):
            if(float(regs[31]/1000)/1000)!=0 and (float(regs[14]/1000)!=0):
                eficiencia = (float(regs[24]/1000)) /(float(regs[31]/1000))
                eficiencia=eficiencia*100
            else:
                eficiencia =0
            dadosEnviar = {
            "cod":i,
            "e_diaria": 1.0, #float(vetor[i-100][2]/10),
            "e_total": 1.0, #float(vetor[i-100][4]),
            "tempo_total": 1.0, #float(vetor[i-100][6]),
            "temperatura_inv": float(regs[33]/10),
            "potencia_total_dc":float(regs[31]/1000),
            "tensao_a": float(regs[10]/10),
            "tensao_b": float(regs[11]/10),
            "tensao_c": float(regs[12]/10),
            "corrente_a": float(regs[3/10]),
            "corrente_b": float(regs[4]/10),
            "corrente_c": float(regs[5]/10),
            "potencia_total_ac": float(regs[14]/1000),
            "fp": float(regs[21]/1000),
            "frequencia": float(regs[16]/10),
            "status": float(regs[38]),
            "bus_volt":a,
            "eficiencia": float(eficiencia),
            "pot_ativa": (float(regs[24]/1000)),
            "pot_reativa": (float(regs[20]/1000)),
            "tensao_combiner": 0,
            "temp_combiner": 0,
            "corrente_max": 0,
            "corrente_media": 0,
            "corrente_total": 0,
            "pot_total_dc": 0,
            "e_diaria_combiner": 0,
            "e_total_combiner":0,
            "alarme": 0,
            "usina_id": 33,
            "modelo": "Modelo XXX",
            "sn": "XXX",
            "pn": "XXX",
            "correntes_string": []
            }
        #Estrutura de repetição para armazenar os dados de 14 "correntes_string"
        p = 1
        for y in range(7,20):
                if(vetor2.get(p)!=None and len(vetor2[p])==84):
                    dadosEnviar["correntes_string"].append({"cod": p,"valor": vetor2[p][y]/100})
                    p += 1   
        # lista com todos os dados para envio    
        listaDados[i-101]=dadosEnviar

    
    #função de envio HTTP
    try:
        asyncio.run(envioPost(listaDados,myUrl,head))
    except:
        print("ERRO no envio: 'Inversores'")

    print("Preparando envio de combiners")
    myUrl = 'https://api-data-receiver.mv-toth.com/combiners'
    #
    # Definir a lista de dados para combiners
    #
    listaDados = [None] * 3
    for i in range(101, 103):
            dados = {
                "cod": i,
                "tensao_combiner": 0,
                "temp_combiner": 0,
                "corrente_max": 0,
                "corrente_media": 0,
                "corrente_total": 0,
                "pot_total_dc": 0,
                "e_diaria_combiner": 0,
                "e_total_combiner": 0,
                "usina_id": 33,
                "correntes_string": [],
                "alarmes": [{
                    "cod": 1,
                    "alarme": 1
                }]    
                }
            #Estrutura de repetição para armazenar os dados de 14 "correntes_string"
        
    for y in range(7,20):
        if(vetor2.get(i)!=None and len(vetor2[i])==84):
            dados["correntes_string"].append({"cod": y-6,"valor": vetor2[i][y]/100})
        # lista com todos os dados para envio
        listaDados[i-101]=dados
        
     
    #função de envio HTTP
    try:
        asyncio.run(envioPost(listaDados,myUrl,head))
    except:
        print("ERRO no envio: 'Combiners'")

