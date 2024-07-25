import wmi
import socket
import psutil
import shutil

def write_to_txt(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for section_title, section_data in data.items():
            file.write(f"{section_title}\n")
            if isinstance(section_data, list):
                for item in section_data:
                    for key, value in item.items():
                        file.write(f"{key}: {value}\n")
                    file.write("\n")
            else:
                for key, value in section_data.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")

def get_system_info():
    try:
        # Conectar ao namespace root/cimv2
        c = wmi.WMI()

        # Dicionários para armazenar os dados
        system_info = {}
        processors_info = []
        ram_info = {}
        disks_info = []
        network_info = {}

        # Obter informações do sistema operacional
        for os in c.Win32_OperatingSystem():
            system_info = {
                "Sistema Operacional": os.Caption,
                "Versão": os.Version,
                "Arquitetura": os.OSArchitecture,
                "ID do Produto": os.SerialNumber,
                "Instalação": os.InstallDate
            }

        # Obter informações dos processadores
        for cpu in c.Win32_Processor():
            processors_info.append({
                "Nome": cpu.Name,
                "Fabricante": cpu.Manufacturer,
                "Núcleos": cpu.NumberOfCores,
                "Frequência Máxima": f"{cpu.MaxClockSpeed} MHz"
            })

        # Obter informações da memória RAM
        total_ram = psutil.virtual_memory().total
        ram_info = {
            "Total RAM (GB)": total_ram / (1024**3)  # Convertendo para GB
        }

        # Obter informações dos discos rígidos
        for disk in c.Win32_DiskDrive():
            disks_info.append({
                "Modelo": disk.Model,
                "Interface": disk.InterfaceType,
                "Capacidade (GB)": int(disk.Size) // (1024**3)  # Convertendo para GB
            })

        # Obter informações da rede
        hostname = socket.gethostname()
        network_info = {
            "Nome do Host": hostname
        }
        ips = socket.gethostbyname_ex(hostname)[2]
        for i, ip in enumerate(ips):
            network_info[f"Endereço IP {i+1}"] = ip

        # Dados a serem escritos no arquivo txt
        data_to_write = {
            "Informações do Sistema Operacional": system_info,
            "Informações dos Processadores": processors_info,
            "Informações da Memória RAM": ram_info,
            "Informações dos Discos Rígidos": disks_info,
            "Informações de Rede": network_info
        }

        # Nome do arquivo de saída
        filename = f"{ips[0]}-{hostname}.txt"

        # Escrever dados no arquivo txt
        write_to_txt(filename, data_to_write)

        print(f"Arquivo TXT gerado com sucesso: {filename}")

        return filename  # Retorna o nome do arquivo gerado

    except Exception as e:
        print(f"Erro ao gerar arquivo TXT: {e}")

if __name__ == "__main__":
    filename = get_system_info()
    if filename:
        # Enviar arquivo para pasta na rede
        destination_folder = r"\\172.16.0.9\LinxPOS-e\inventory"
        shutil.copy(filename, destination_folder)
        print(f"Arquivo TXT enviado para: {destination_folder}")
