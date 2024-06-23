import requests
import threading
import time
import tkinter as tk
from tkinter import messagebox
import configparser
import ast
import os

# URL do arquivo raw no GitHub
github_raw_url = 'https://raw.githubusercontent.com/danielhito102/Update-Macro/main/main.py'

# Caminho local para salvar o arquivo atualizado
local_file_path = 'main.py'

# Função para baixar o conteúdo do arquivo do GitHub
def download_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            print(f'Falha ao baixar o arquivo {url}: Status {response.status_code}')
            return None
    except Exception as e:
        print(f'Erro ao baixar o arquivo {url}: {str(e)}')
        return None

# Função para verificar e aplicar atualizações
def check_for_update():
    while True:
        try:
            current_content = download_file(github_raw_url)
            if current_content:
                with open(local_file_path, 'r', encoding='utf-8') as f:
                    local_content = f.read()

                if current_content != local_content:
                    print("Nova versão encontrada. Atualizando...")
                    with open(local_file_path, 'w', encoding='utf-8') as f:
                        f.write(current_content)
                    apply_update()

            time.sleep(60)  # Verificar a cada 60 segundos
        except Exception as e:
            print(f"Erro ao verificar atualizações: {str(e)}")
            time.sleep(60)

# Função para aplicar as atualizações dinamicamente
def apply_update():
    try:
        with open(local_file_path, 'r', encoding='utf-8') as f:
            updated_code = f.read()
        
        # Executar o código atualizado dinamicamente
        exec(updated_code, globals())
        print("Atualização aplicada com sucesso!")
    except Exception as e:
        print(f"Erro ao aplicar atualização: {str(e)}")

# Thread para verificação de atualizações
update_thread = threading.Thread(target=check_for_update)
update_thread.daemon = True
update_thread.start()

# Inicialização da GUI
gui = tk.Tk()
gui.title("Macro de Controle de Recuo")

# Variável para armazenar a hotkey (exemplo)
hotkey = 'F1'

# Funções para o GUI (exemplo)
def setValues():
    pass

def toggleAimCheck():
    pass

def saveLoadout():
    pass

def loadLoadout():
    pass

# Labels e botões do GUI (exemplo)
tk.Label(gui, text='Configurações da Macro').pack()

tk.Button(gui, text="Definir", command=setValues).pack()

tk.Button(gui, text="Salvar Loadout", command=saveLoadout).pack()

tk.Button(gui, text="Carregar Loadout", command=loadLoadout).pack()

tk.Label(gui, text=f'Pressione {hotkey} para iniciar/parar a macro.').pack()

# Laço principal da GUI
gui.mainloop()
