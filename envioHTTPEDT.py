#EDT

from argparse import _VersionAction
from dataclasses import dataclass
import aiohttp
import asyncio
import json


#
# Função para envio dos dados em HTTP (request.post)
# 
async def envioPost(dado):
    async with aiohttp.ClientSession(headers=head) as session:
        async with session.post(myUrl,json=dado) as resp:
            print("Codigo de resposta: <",resp.status,">")


#
# Informações fundamentais para a comunicação com o servidor (token url e cabeçalho)
#
myToken = 'NKick68KLONcwzcRMS3KZyI7m4g5xoJwvDcsmS46JDhECTmFaSuhr0ew53yRW5t8f8wIjdpfScR8tRcjEWa8gXiDhVwtAsk9r0Q9oYRjyWoYP9VnMxUvPQnY'
myUrl = 'https://api-data-receiver.mv-toth.com/energies'
head = {'X-API-KEY':myToken}

def envio_EDT(dado):
    print("Preparando envio de EDT")
    #
    # Definir a lista de dados
    #
    listaDados = {
           "energia": dado,
           "usina_id": 33,
    }

    #função de envio HTTP
    try:
        asyncio.run(envioPost(listaDados))
    except:
        print("ERRO no envio: 'EDT'")
