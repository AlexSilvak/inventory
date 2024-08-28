import wmi
import socket
import psutil
import requests
from datetime import datetime
import json
import math

#Endpoint
endpoint_url = "http://localhost:5000/api/devices"


def get_last_id_from_endpoint(endpoint_url):
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data:
            ids = map(lambda item: item.get('id'), data)
            valid_ids = filter(lambda x: isinstance(x, int), ids)
            last_id = max(valid_ids, default=0)
        else:
            last_id = 0  # Caso não haja dados válidos ou a lista esteja vazia

        return last_id + 1  # Retornar o próximo ID

    except requests.RequestException as e:
        print(f"Erro ao obter o último ID do endpoint: {e}")
        return 1  # Retornar o ID inicial 1 em caso de erro



def get_system_info():
    try:
        c = wmi.WMI()

        # Obter informações do sistema operacional
        for os in c.Win32_OperatingSystem():
            system_info = {
                "Sistema Operacional": os.Caption,
                "Versão": os.Version,
                "Arquitetura": os.OSArchitecture,
               
                
            }
           

        # Informações dos Processadores
        cpu_info = c.Win32_Processor()[0]
        processor_info = cpu_info.Name

        # Memória RAM
        total_ram = psutil.virtual_memory().total / (1024**3)  # Convertendo para GB
        ram_info = total_ram

        # Discos Rígidos
        disk_info = c.Win32_DiskDrive()[0]
        disk_model = disk_info.Model
        disk_capacity = int(disk_info.Size) // (1024**3)  # Convertendo para GB

        # Rede
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        #Gereração de ID
        newID=get_last_id_from_endpoint(endpoint_url)
        # Dados para enviar
        data_to_send = {
    "id":f'{newID}',
	"sistema_operacional": f'{system_info}',
	"processador": f'{processor_info}',
	"memoria_ram":f'{ram_info}',
	"disco_modelo":f'{disk_model}',
	"disco_capacidade":f'{disk_capacity}',
	"device_name": f'{hostname}',
	"ip":f'{ip_address}',
	"status":"true"
        }

        return data_to_send

    except Exception as e:
        print(f"Erro ao obter informações do sistema: {e}")
        return None

def send_data_to_endpoint(data, endpoint_url):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(endpoint_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida
        print(f"Dados enviados para: {endpoint_url}")
        print(f"Resposta do servidor: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Erro ao enviar dados para o endpoint: {e}")

if __name__ == "__main__":
    data = get_system_info()
    if data:
        
        send_data_to_endpoint(data, endpoint_url)
