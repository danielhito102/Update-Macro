import requests
import threading
import time
import tkinter as tk
from tkinter import messagebox
import configparser
import ast
import os
import subprocess
import sys

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
                    restart_program()

            time.sleep(60)  # Verificar a cada 60 segundos
        except Exception as e:
            print(f"Erro ao verificar atualizações: {str(e)}")
            time.sleep(60)

# Função para reiniciar o programa
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Thread para verificação de atualizações
update_thread = threading.Thread(target=check_for_update)
update_thread.daemon = True
update_thread.start()

# Inicialização da GUI
gui = tk.Tk()
gui.title("Macro de Controle de Recuo")

# Variáveis para armazenar os valores das configurações (exemplo)
xValue = 0
yValue = 0
delayValue = 10
recoilFactor = 1.0
speedX = 0.5
speedY = 2.0
accelerationX = 0.5
accelerationY = 0.5
aimCheck = False

# Funções para o GUI (exemplo)
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
        delay.set(loadoutList[2])
        recoil.set(loadoutList[3])

    except configparser.NoOptionError:
        messagebox.showwarning("Erro", f"Nenhum loadout chamado {name} encontrado")
    except ValueError as e:
        messagebox.showerror("Erro", f"Erro ao carregar loadout {name}: {str(e)}")
    except SyntaxError:
        messagebox.showerror("Erro", f"Erro ao carregar loadout {name}. Sintaxe inválida.")

# Labels e botões do GUI (exemplo)
tk.Label(gui, text='Configurações da Macro').pack()

aimCheckButton = tk.Button(gui, text="Aim Check Desligado", command=toggleAimCheck)
aimCheckButton.pack()

tk.Label(gui, text='Controle X').pack()
xControl = tk.Scale(gui, from_=-50, to=50, orient=tk.HORIZONTAL, length=200)
xControl.pack()

tk.Label(gui, text='Controle Y').pack()
yControl = tk.Scale(gui, from_=0, to=100, orient=tk.VERTICAL, length=200)
yControl.set(1)
yControl.pack()

tk.Label(gui, text='Atraso entre Movimentos (ms)').pack()
delay = tk.Scale(gui, from_=1, to=50, orient=tk.HORIZONTAL, length=150)
delay.set(10)
delay.pack()

tk.Label(gui, text='Fator de Recuo').pack()
recoil = tk.Scale(gui, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
recoil.set(1.0)
recoil.pack()

tk.Label(gui, text='Velocidade Horizontal').pack()
speedXControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
speedXControl.set(speedX)
speedXControl.pack()

tk.Label(gui, text='Aceleração Horizontal').pack()
accelerationXControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
accelerationXControl.set(accelerationX)
accelerationXControl.pack()

tk.Label(gui, text='Velocidade Vertical').pack()
speedYControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
speedYControl.set(speedY)
speedYControl.pack()

tk.Label(gui, text='Aceleração Vertical').pack()
accelerationYControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
accelerationYControl.set(accelerationY)
accelerationYControl.pack()

setButton = tk.Button(gui, text="Definir", command=setValues)
setButton.pack()

tk.Label(gui, text=f'Pressione F1 para iniciar/parar a macro.').pack()

loadoutName = tk.Entry(gui)
loadoutName.pack()

saveButton = tk.Button(gui, text='Salvar Loadout', command=saveLoadout)
saveButton.pack()

loadButton = tk.Button(gui, text='Carregar Loadout', command=loadLoadout)
loadButton.pack()

# Laço principal da GUI
gui.mainloop()
