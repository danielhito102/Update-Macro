import keyboard
import mouse
import tkinter as tk
from tkinter import messagebox
import screeninfo
import configparser
import os
import time
import threading
import ctypes
import ast
import math
import requests
import subprocess
import sys

# Configuração inicial do arquivo de configuração e GUI tkinter
aimCheck = False

xValue = 0
yValue = 0
delayValue = 10  # Atraso entre movimentos em 10 ms
recoilFactor = 1.0
speedX = 0.5  # Velocidade horizontal
speedY = 2.0  # Velocidade vertical
accelerationX = 0.5  # Aceleração horizontal
accelerationY = 0.5  # Aceleração vertical em 0.5

# Variável para armazenar a última posição do clique esquerdo
last_left_click_position = (0, 0)

# Verifica se o arquivo de configuração existe; se não, cria um novo
if not os.path.isfile('config.txt'):
    print('Arquivo config.txt não encontrado. Criando um novo...')
    config = configparser.ConfigParser()
    config['hotkey'] = {'hotkey': 'p'}
    config['loadouts'] = {}
    with open('config.txt', 'w') as fp:
        config.write(fp)
    print('Arquivo config.txt criado com sucesso.')

# Carrega as configurações do arquivo config.txt
config = configparser.ConfigParser()
config.read('config.txt')

# Verifica se a seção 'hotkey' existe e se 'hotkey' está configurada
if 'hotkey' not in config or 'hotkey' not in config['hotkey']:
    print('Hotkey não encontrada. Adicionando linha de hotkey ao arquivo de configuração...')
    config['hotkey'] = {'hotkey': 'p'}
    config['loadouts'] = {}
    with open('config.txt', 'w') as fp:
        config.write(fp)
    print('Hotkey configurada como "p" por padrão.')

# Obtém a hotkey configurada
hotkey = config['hotkey']['hotkey']
print('Hotkey definida como:', hotkey)

def setValues():
    global xValue, yValue, delayValue, recoilFactor, speedX, speedY, accelerationX, accelerationY
    xValue = xControl.get() * speedX
    yValue = 1 * speedY  # Valor fixo de 1 para controle Y
    delayValue = delay.get()
    recoilFactor = recoil.get()
    accelerationX = accelerationXControl.get()
    accelerationY = accelerationYControl.get()
    print(f"Valores definidos - X:{xValue} Y:{yValue} D:{delayValue} Fator de Recuo:{recoilFactor}")

def toggleAimCheck():
    global aimCheck
    if aimCheck:
        aimCheck = False
        aimCheckButton.config(text='Aim Check Desligado')
    else:
        aimCheck = True
        aimCheckButton.config(text='Aim Check Ligado')

def getResolution():
    screens = screeninfo.get_monitors()
    primary_monitor = screens[0]
    return primary_monitor.width, primary_monitor.height

def saveLoadout():
    setValues()
    name = str(loadoutName.get())
    loadoutName.delete(0, tk.END)
    config = configparser.ConfigParser()
    config.read('config.txt')
    if not config.has_section('loadouts'):
        config.add_section('loadouts')
    config.set('loadouts', name, f'[{xValue},{yValue},{delayValue},{recoilFactor}]')
    with open('config.txt', 'w') as fp:
        config.write(fp)

def loadLoadout():
    global xValue, yValue, delayValue, recoilFactor, speedX, speedY, accelerationX, accelerationY
    setValues()
    name = str(loadoutName.get())
    loadoutName.delete(0, tk.END)
    config = configparser.ConfigParser()
    config.read('config.txt')

    try:
        loadout = config.get('loadouts', name)
        loadoutList = ast.literal_eval(loadout)
        if len(loadoutList) != 4:
            raise ValueError("Loadout não possui 4 elementos")

        xValue = loadoutList[0]
        yValue = loadoutList[1]
        delayValue = loadoutList[2]
        recoilFactor = loadoutList[3]

        xControl.set(loadoutList[0])
        # yControl.set(loadoutList[1])  # Não ajusta o controle Y, que fica fixo em 1
        delay.set(loadoutList[2])
        recoil.set(loadoutList[3])

    except configparser.NoOptionError:
        messagebox.showwarning("Erro", f"Nenhum loadout chamado {name} encontrado")
    except ValueError as e:
        messagebox.showerror("Erro", f"Erro ao carregar loadout {name}: {str(e)}")
    except SyntaxError:
        messagebox.showerror("Erro", f"Erro ao carregar loadout {name}. Sintaxe inválida.")

def check_for_updates():
    try:
        github_url = 'https://raw.githubusercontent.com/danielhito102/Update-Macro/main/update.py'
        response = requests.head(github_url)
        
        if 'Last-Modified' in response.headers:
            new_last_modified = response.headers['Last-Modified']
            
            if 'last_modified' not in globals() or new_last_modified != globals()['last_modified']:
                print("Detectada uma modificação no arquivo update.py. Atualizando...")
                
                response = requests.get(github_url)
                
                with open('update.py', 'wb') as file:
                    file.write(response.content)
                
                globals()['last_modified'] = new_last_modified
                
                print("Arquivo update.py atualizado. Reiniciando o programa...")
                restart_program()
        else:
            print("Cabeçalho 'Last-Modified' não encontrado na resposta.")
    
    except Exception as e:
        print(f"Erro ao verificar/atualizar: {e}")
    
    time.sleep(60)  # Verifica a cada 60 segundos

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Funções de GUI e macro continuam aqui...

gui = tk.Tk()
gui.title("Macro de Controle de Recuo")

# Código da interface gráfica e macro continua aqui...

# Função principal para verificar atualizações em segundo plano
def check_updates_thread():
    while True:
        check_for_updates()

# Thread para verificar atualizações em segundo plano
update_thread = threading.Thread(target=check_updates_thread)
update_thread.daemon = True
update_thread.start()

# Código da macro e execução da GUI
# ...

# Código da macro e execução da GUI continua aqui...

gui.mainloop()
