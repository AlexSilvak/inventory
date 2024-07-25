import os

def limpar_fila_impressao():
    try:
        os.system('net stop spooler')  # Para o serviço de spooler de impressão
        os.system('del /Q /F /S %systemroot%\\System32\\Spool\\Printers\\*')  # Exclui todos os arquivos na pasta de spool
        os.system('net start spooler')  # Inicia o serviço de spooler de impressão novamente
        print("Fila de impressão limpa com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao limpar a fila de impressão: {str(e)}")

# Chamada da função para limpar a fila de impressão
limpar_fila_impressao()
