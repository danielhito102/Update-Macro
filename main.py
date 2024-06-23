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
def check_for_update(gui):
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
                    # Atualizar a GUI principal
                    gui.update_gui()

            time.sleep(60)  # Verificar a cada 60 segundos
        except Exception as e:
            print(f"Erro ao verificar atualizações: {str(e)}")
            time.sleep(60)

# Função para reiniciar o programa
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Classe principal da GUI
class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro de Controle de Recuo")

        # Variáveis para armazenar os valores das configurações (exemplo)
        self.xValue = 0
        self.yValue = 0
        self.delayValue = 10
        self.recoilFactor = 1.0
        self.speedX = 0.5
        self.speedY = 2.0
        self.accelerationX = 0.5
        self.accelerationY = 0.5
        self.aimCheck = False

        # Labels e botões do GUI (exemplo)
        tk.Label(root, text='Configurações da Macro').pack()

        self.aimCheckButton = tk.Button(root, text="Aim Check Desligado", command=self.toggle_aim_check)
        self.aimCheckButton.pack()

        tk.Label(root, text='Controle X').pack()
        self.xControl = tk.Scale(root, from_=-50, to=50, orient=tk.HORIZONTAL, length=200)
        self.xControl.pack()

        tk.Label(root, text='Controle Y').pack()
        self.yControl = tk.Scale(root, from_=0, to=100, orient=tk.VERTICAL, length=200)
        self.yControl.set(1)
        self.yControl.pack()

        tk.Label(root, text='Atraso entre Movimentos (ms)').pack()
        self.delay = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL, length=150)
        self.delay.set(10)
        self.delay.pack()

        tk.Label(root, text='Fator de Recuo').pack()
        self.recoil = tk.Scale(root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
        self.recoil.set(1.0)
        self.recoil.pack()

        tk.Label(root, text='Velocidade Horizontal').pack()
        self.speedXControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
        self.speedXControl.set(self.speedX)
        self.speedXControl.pack()

        tk.Label(root, text='Aceleração Horizontal').pack()
        self.accelerationXControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
        self.accelerationXControl.set(self.accelerationX)
        self.accelerationXControl.pack()

        tk.Label(root, text='Velocidade Vertical').pack()
        self.speedYControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
        self.speedYControl.set(self.speedY)
        self.speedYControl.pack()

        tk.Label(root, text='Aceleração Vertical').pack()
        self.accelerationYControl = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=150)
        self.accelerationYControl.set(self.accelerationY)
        self.accelerationYControl.pack()

        self.setButton = tk.Button(root, text="Definir", command=self.set_values)
        self.setButton.pack()

        tk.Label(root, text=f'Pressione F1 para iniciar/parar a macro.').pack()

        self.loadoutName = tk.Entry(root)
        self.loadoutName.pack()

        self.saveButton = tk.Button(root, text='Salvar Loadout', command=self.save_loadout)
        self.saveButton.pack()

        self.loadButton = tk.Button(root, text='Carregar Loadout', command=self.load_loadout)
        self.loadButton.pack()

    def set_values(self):
        self.xValue = self.xControl.get() * self.speedX
        self.yValue = 1 * self.speedY  # Valor fixo de 1 para controle Y
        self.delayValue = self.delay.get()
        self.recoilFactor = self.recoil.get()
        self.accelerationX = self.accelerationXControl.get()
        self.accelerationY = self.accelerationYControl.get()
        print(f"Valores definidos - X:{self.xValue} Y:{self.yValue} D:{self.delayValue} Fator de Recuo:{self.recoilFactor}")

    def toggle_aim_check(self):
        self.aimCheck = not self.aimCheck
        if self.aimCheck:
            self.aimCheckButton.config(text='Aim Check Ligado')
        else:
            self.aimCheckButton.config(text='Aim Check Desligado')

    def save_loadout(self):
        self.set_values()
        name = str(self.loadoutName.get())
        self.loadoutName.delete(0, tk.END)
        config = configparser.ConfigParser()
        config.read('config.txt')
        if not config.has_section('loadouts'):
            config.add_section('loadouts')
        config.set('loadouts', name, f'[{self.xValue},{self.yValue},{self.delayValue},{self.recoilFactor}]')
        with open('config.txt', 'w') as fp:
            config.write(fp)

    def load_loadout(self):
        name = str(self.loadoutName.get())
        self.loadoutName.delete(0, tk.END)
        config = configparser.ConfigParser()
        config.read('config.txt')

        try:
            loadout = config.get('loadouts', name)
            loadout_list = ast.literal_eval(loadout)
            if len(loadout_list) != 4:
                raise ValueError("Loadout não possui 4 elementos")

            self.xValue = loadout_list[0]
            self.yValue = loadout_list[1]
            self.delayValue = loadout_list[2]
            self.recoilFactor = loadout_list[3]

            self.xControl.set(loadout_list[0])
            self.delay.set(loadout_list[2])
            self.recoil.set(loadout_list[3])

            print(f"Loadout {name} carregado com sucesso.")
        except configparser.NoOptionError:
            messagebox.showwarning("Erro", f"Nenhum loadout chamado {name} encontrado")
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao carregar loadout {name}: {str(e)}")
        except SyntaxError:
            messagebox.showerror("Erro", f"Erro ao carregar loadout {name}. Sintaxe inválida.")

    def update_gui(self):
        # Atualiza os valores nos controles da GUI conforme os novos valores
        self.xControl.set(self.xValue)
        self.delay.set(self.delayValue)
        self.recoil.set(self.recoilFactor)
        # Adicione aqui outros controles que precisam ser atualizados

def main():
    # Inicializa a GUI principal
    root = tk.Tk()
    gui = MainGUI(root)

    # Verifica e inicia a atualização em uma thread separada, passando o objeto gui como parâmetro
    update_thread = threading.Thread(target=check_for_update, args=(gui,))
    update_thread.daemon = True
    update_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
