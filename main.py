import requests
import threading
import time
import tkinter as tk
from tkinter import messagebox
import configparser
import ast

# URL do arquivo raw no GitHub
github_raw_url = 'https://raw.githubusercontent.com/danielhito102/Update-Macro/main/config.txt'

# Caminho local para salvar o arquivo atualizado
local_file_path = 'config.txt'

# Variáveis globais para armazenar os valores das configurações
xValue = 0
yValue = 0
delayValue = 10
recoilFactor = 1.0
speedX = 0.5
speedY = 2.0
accelerationX = 0.5
accelerationY = 0.5
aimCheck = False

# Inicialização da GUI
root = tk.Tk()
root.title("Macro de Controle de Recuo")

# Labels e botões do GUI (exemplo)
tk.Label(root, text='Configurações da Macro').pack()

# Função para definir os valores das configurações
def set_values():
    global xValue, yValue, delayValue, recoilFactor, speedX, speedY, accelerationX, accelerationY
    xValue = xControl.get() * speedX
    yValue = 1 * speedY  # Valor fixo de 1 para controle Y
    delayValue = delay.get()
    recoilFactor = recoil.get()
    accelerationX = accelerationXControl.get()
    accelerationY = accelerationYControl.get()
    print(f"Valores definidos - X:{xValue} Y:{yValue} D:{delayValue} Fator de Recuo:{recoilFactor}")

# Função para alternar o Aim Check
def toggle_aim_check():
    global aimCheck
    if aimCheck:
        aimCheck = False
        aimCheckButton.config(text='Aim Check Desligado')
    else:
        aimCheck = True
        aimCheckButton.config(text='Aim Check Ligado')

# Função para salvar o Loadout
def save_loadout():
    set_values()
    name = str(loadoutName.get())
    loadoutName.delete(0, tk.END)
    config = configparser.ConfigParser()
    config.read(local_file_path)
    if not config.has_section('loadouts'):
        config.add_section('loadouts')
    config.set('loadouts', name, f'[{xValue},{yValue},{delayValue},{recoilFactor}]')
    with open(local_file_path, 'w') as fp:
        config.write(fp)

# Função para carregar o Loadout
def load_loadout():
    global xValue, yValue, delayValue, recoilFactor, speedX, speedY, accelerationX, accelerationY
    set_values()
    name = str(loadoutName.get())
    loadoutName.delete(0, tk.END)
    config = configparser.ConfigParser()
    config.read(local_file_path)

    try:
        loadout = config.get('loadouts', name)
        loadout_list = ast.literal_eval(loadout)
        if len(loadout_list) != 4:
            raise ValueError("Loadout não possui 4 elementos")

        xValue = loadout_list[0]
        yValue = loadout_list[1]
        delayValue = loadout_list[2]
        recoilFactor = loadout_list[3]

        xControl.set(loadout_list[0])
        delay.set(loadout_list[2])
        recoil.set(loadout_list[3])

    except configparser.NoOptionError:
        messagebox.showwarning("Erro", f"Nenhum loadout chamado {name} encontrado")
    except ValueError as e:
        messagebox.showerror("Erro", f"Erro ao carregar loadout {name}: {str(e)}")
    except SyntaxError:
        messagebox.showerror("Erro", f"Erro ao carregar loadout {name}. Sintaxe inválida.")

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
    global xValue, yValue, delayValue, recoilFactor, speedX, speedY, accelerationX, accelerationY, aimCheck
    current_content = download_file(github_raw_url)
    if current_content:
        with open(local_file_path, 'r', encoding='utf-8') as f:
            local_content = f.read()

        if current_content != local_content:
            print("Nova versão encontrada. Atualizando...")
            try:
                config = ast.literal_eval(current_content)
                xValue = config.get('xValue', xValue)
                yValue = config.get('yValue', yValue)
                delayValue = config.get('delayValue', delayValue)
                recoilFactor = config.get('recoilFactor', recoilFactor)
                speedX = config.get('speedX', speedX)
                speedY = config.get('speedY', speedY)
                accelerationX = config.get('accelerationX', accelerationX)
                accelerationY = config.get('accelerationY', accelerationY)
                aimCheck = config.get('aimCheck', aimCheck)

                update_gui()
                print("Valores atualizados com sucesso.")
            except Exception as e:
                print(f"Erro ao atualizar valores: {str(e)}")

    # Verifica novamente após 60 segundos
    threading.Timer(60, check_for_update).start()

# Função para atualizar a GUI com os novos valores
def update_gui():
    global xControl, yControl, delay, recoil, speedXControl, accelerationXControl, speedYControl, accelerationYControl
    # Atualizar todos os controles da GUI com os novos valores das variáveis globais
    xControl.set(xValue)
    yControl.set(yValue)
    delay.set(delayValue)
    recoil.set(recoilFactor)
    speedXControl.set(speedX)
    speedYControl.set(speedY)
    accelerationXControl.set(accelerationX)
    accelerationYControl.set(accelerationY)
    if aimCheck:
        aimCheckButton.config(text='Aim Check Ligado')
    else:
        aimCheckButton.config(text='Aim Check Desligado')

# Labels e botões do GUI (exemplo)
tk.Label(root, text='Controle X').pack()
xControl = tk.Scale(root, from_=-50, to=50, orient=tk.HORIZONTAL, length=200)
xControl.pack()

tk.Label(root, text='Controle Y').pack()
yControl = tk.Scale(root, from_=0, to=100, orient=tk.VERTICAL, length=200)
yControl.set(1)
yControl.pack()

tk.Label(root, text='Atraso entre Movimentos (ms)').pack()
delay = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL, length=150)
delay.set(10)
delay.pack()

tk.Label(root, text='Fator de Recuo').pack()
recoil = tk.Scale(root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
recoil.set(1.0)
recoil.pack()

tk.Label(root, text='Velocidade Horizontal').pack()
speedXControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
speedXControl.set(speedX)
speedXControl.pack()

tk.Label(root, text='Aceleração Horizontal').pack()
accelerationXControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
accelerationXControl.set(accelerationX)
accelerationXControl.pack()

tk.Label(root, text='Velocidade Vertical').pack()
speedYControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
speedYControl.set(speedY)
speedYControl.pack()

tk.Label(root, text='Aceleração Vertical').pack()
accelerationYControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
accelerationYControl.set(accelerationY)
accelerationYControl.pack()

aimCheckButton = tk.Button(root, text="Aim Check Desligado", command=toggle_aim_check)
aimCheckButton.pack()

tk.Label(root, text=f'Pressione F1 para iniciar/parar a macro.').pack()

loadoutName = tk.Entry(root)
loadoutName.pack()

saveButton = tk.Button(root, text='Salvar Loadout', command=save_loadout)
saveButton.pack()

loadButton = tk.Button(root, text='Carregar Loadout', command=load_loadout)
loadButton.pack()

# Thread para verificação de atualizações
check_for_update()

# Laço principal da GUI
root.mainloop()
