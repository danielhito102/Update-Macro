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
import hashlib

# URL do arquivo no GitHub
github_raw_url = "https://raw.githubusercontent.com/danielhito102/Update-Macro/main/update.py"

# Nome do arquivo local
local_file_name = "update.py"

# Função para baixar o conteúdo do GitHub
def download_from_github(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Erro ao baixar o código do GitHub. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro durante a requisição para baixar o código do GitHub: {str(e)}")
        return None

# Função para comparar hashes SHA-256
def calculate_sha256(file_path):
    try:
        with open(file_path, "rb") as file:
            file_hash = hashlib.sha256()
            while chunk := file.read(4096):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except FileNotFoundError:
        return None

# Verificar se o arquivo local existe e baixar/atualizar se necessário
if os.path.isfile(local_file_name):
    # Calcular hash SHA-256 do arquivo local
    local_hash = calculate_sha256(local_file_name)

    # Baixar o conteúdo atual do GitHub
    github_code = download_from_github(github_raw_url)

    if github_code:
        # Calcular hash SHA-256 do conteúdo baixado
        github_hash = hashlib.sha256(github_code.encode('utf-8')).hexdigest()

        # Comparar hashes SHA-256
        if local_hash != github_hash:
            print("O código local está desatualizado. Atualizando para a versão mais recente...")

            # Escrever o conteúdo baixado no arquivo local
            with open(local_file_name, "w", encoding='utf-8') as file:
                file.write(github_code)

            print("Atualização concluída.")
        else:
            print("O código local já está atualizado.")
    else:
        print("Não foi possível baixar o código do GitHub. Verifique sua conexão com a internet.")
else:
    # Se o arquivo local não existir inicialmente, baixar o conteúdo do GitHub diretamente
    github_code = download_from_github(github_raw_url)
    
    if github_code:
        # Escrever o conteúdo baixado no arquivo local
        with open(local_file_name, "w", encoding='utf-8') as file:
            file.write(github_code)
            
        print("Arquivo local criado com a versão mais recente do GitHub.")
    else:
        print("Não foi possível baixar o código do GitHub. Verifique sua conexão com a internet.")

# Configuração inicial do arquivo de configuração e GUI tkinter
aimCheck = False

xValue = 0
yValue = 0
delayValue = 1  # Atraso entre movimentos em 10 ms
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

gui = tk.Tk()
gui.title("Macro de Controle de Recuo")

tk.Label(gui, text="").pack()

aimCheckButton = tk.Button(gui, text="Aim Check Desligado", command=toggleAimCheck)
aimCheckButton.pack()

label = tk.Label(gui, text='Controle X')
label.pack()

xControl = tk.Scale(gui, from_=-50, to=50, orient=tk.HORIZONTAL, length=200)
xControl.pack()

tk.Label(gui, text="").pack()

label = tk.Label(gui, text='Controle Y')
label.pack()

yControl = tk.Scale(gui, from_=0, to=100, orient=tk.VERTICAL, length=200)
yControl.set(1)  # Fixa o controle Y em 1
yControl.pack()

tk.Label(gui, text="").pack()

label = tk.Label(gui, text='Atraso entre Movimentos (ms)')
label.pack()

delay = tk.Scale(gui, from_=1, to=50, orient=tk.HORIZONTAL, length=150)
delay.set(10)  # Alterado para 10 ms
delay.pack()

tk.Label(gui, text="").pack()

label = tk.Label(gui, text='Fator de Recuo')
label.pack()

recoil = tk.Scale(gui, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
recoil.set(1.0)  # Fixa o fator de recuo em 1.0
recoil.pack()

tk.Label(gui, text="").pack()

# Adicionando controles de velocidade e aceleração
label = tk.Label(gui, text='Velocidade Horizontal')
label.pack()

speedXControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
speedXControl.set(speedX)
speedXControl.pack()

tk.Label(gui, text="").pack()

label = tk.Label(gui, text='Aceleração Horizontal')
label.pack()

accelerationXControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
accelerationXControl.set(accelerationX)
accelerationXControl.pack()

tk.Label(gui, text="").pack()

label = tk.Label(gui, text='Velocidade Vertical')
label.pack()

speedYControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
speedYControl.set(speedY)
speedYControl.pack()

tk.Label(gui, text="").pack()

label = tk.Label(gui, text='Aceleração Vertical')
label.pack()

accelerationYControl = tk.Scale(gui, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
accelerationYControl.set(accelerationY)  # Aceleração vertical alterada para 0.5
accelerationYControl.pack()

tk.Label(gui, text="").pack()

setButton = tk.Button(gui, text="Definir", command=setValues)
setButton.pack()

tk.Label(gui, text="").pack()

tk.Label(gui, text=f'Pressione {hotkey} para iniciar/parar a macro.').pack()
tk.Label(gui, text='Verifique o arquivo config.txt para alterar a hotkey e editar loadouts manualmente.').pack()

tk.Label(gui, text="").pack()

loadoutName = tk.Entry(gui)
loadoutName.pack()

saveButton = tk.Button(gui, text='Salvar Loadout', command=saveLoadout)
saveButton.pack()

loadButton = tk.Button(gui, text='Carregar Loadout', command=loadLoadout)
loadButton.pack()

x, y = getResolution()
largura = int(x / 5)
altura = int(y / 1.5)
gui.geometry(f'{largura}x{altura}')

# Código da macro

habilitado = False

def ajustarRecoil(x, y, fator_recoil):
    ajuste_x = x + math.ceil(x * fator_recoil)
    ajuste_y = y + math.ceil(y * fator_recoil)
    return ajuste_x, ajuste_y

def moveRel(x, y, fator_recoil):
    global last_left_click_position

    currentX, currentY = mouse.get_position()

    if leftClicked():
        last_left_click_position = (currentX, currentY)

    if fator_recoil > 0.0:
        adjusted_x = int(x * speedX * accelerationX + math.ceil(x * fator_recoil))
        adjusted_y = int(y * speedY * accelerationY + math.ceil(y * fator_recoil))
    else:
        adjusted_x = int(x * speedX * accelerationX)
        adjusted_y = int(y * speedY * accelerationY)

    new_x = currentX + adjusted_x
    new_y = currentY + adjusted_y

    ctypes.windll.user32.mouse_event(0x0001, adjusted_x, adjusted_y, 0, 0)

def toggleMacro():
    global habilitado
    if habilitado:
        habilitado = False
        print('Macro Desativada!')
        ctypes.windll.user32.MessageBeep(0x00000010)
    else:
        habilitado = True
        print('Macro Ativada!')
        ctypes.windll.user32.MessageBeep(0xFFFFFFFF)

keyboard.add_hotkey(hotkey, toggleMacro)

def leftClicked():
    if ctypes.windll.user32.GetAsyncKeyState(0x01) != 0:
        return True
    else:
        return False

def rightClicked():
    if ctypes.windll.user32.GetAsyncKeyState(0x02) != 0:
        return True
    else:
        return False

def macroTask():
    while True:
        if habilitado:
            if aimCheck == False and leftClicked():
                moveRel(xValue, yValue, recoilFactor)
            elif aimCheck == True and leftClicked() and rightClicked():
                moveRel(xValue, yValue, recoilFactor)
        time.sleep(delayValue / 1000)

thread = threading.Thread(target=macroTask)
thread.daemon = True
thread.start()

gui.mainloop()
