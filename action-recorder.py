import pyautogui
import keyboard
import time
import pickle
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from threading import Thread
from pynput.mouse import Listener as MouseListener

# Variável global para controle de parada da gravação
stop_gravacao = False
acoes = []
delay = 0  # Delay inicial de 0 segundos

# Função para carregar as ações gravadas de um arquivo
def carregar_acoes():
    try:
        with open('acoes_gravadas.pkl', 'rb') as f:
            acoes = pickle.load(f)

        # Limpa a Listbox antes de carregar as novas ações
        actions_listbox.delete(0, tk.END)

        # Exibe as ações carregadas na Listbox
        for acao in acoes:
            if acao['evento'] == 'teclado':
                actions_listbox.insert(tk.END, f"Tecla pressionada: {acao['tecla']}")
            elif acao['evento'] == 'teclado_atalho':
                actions_listbox.insert(tk.END, f"Atalho pressionado: {acao['comando']}")
            elif acao['evento'] == 'mouse_click':
                actions_listbox.insert(tk.END, f"Mouse clicado em {acao['posicao']} com o botão {acao['botao']}")
            elif acao['evento'] == 'sleep':
                actions_listbox.insert(tk.END, f"Sleep por {acao['tempo']} segundos")
        
        status_label.config(text="Ações carregadas com sucesso!")
        reproduzir_button.config(state=tk.NORMAL)  # Ativa o botão "Reproduzir"
    except FileNotFoundError:
        messagebox.showerror("Erro", "Nenhuma gravação encontrada!")

# Função para gravar as ações
def gravar_acao():
    global acoes, stop_gravacao
    acoes = []
    status_label.config(text="Gravando... Pressione 'esc' para parar.")
    
    # Função para capturar eventos de teclado
    def on_keyboard_event(event):
        if event.event_type == "down" and not stop_gravacao:  # Apenas captura eventos se a gravação não for parada
            if keyboard.is_pressed('ctrl+c'):
                acao = {'evento': 'teclado_atalho', 'comando': 'Ctrl+C'}
                acoes.append(acao)
                actions_listbox.insert(tk.END, f"Atalho pressionado: Ctrl+C")
            elif keyboard.is_pressed('ctrl+v'):
                acao = {'evento': 'teclado_atalho', 'comando': 'Ctrl+V'}
                acoes.append(acao)
                actions_listbox.insert(tk.END, f"Atalho pressionado: Ctrl+V")
            elif event.name == 'enter':
                acao = {'evento': 'teclado', 'tecla': 'Enter'}
                acoes.append(acao)
                actions_listbox.insert(tk.END, "Tecla pressionada: Enter")
            else:
                acao = {'evento': 'teclado', 'tecla': event.name}
                acoes.append(acao)
                actions_listbox.insert(tk.END, f"Tecla pressionada: {event.name}")

    # Função para capturar cliques do mouse
    def on_click(x, y, button, pressed):
        if pressed and not stop_gravacao:  # Verifica a flag antes de capturar o clique
            acao = {'evento': 'mouse_click', 'posicao': (x, y), 'botao': button.name}
            acoes.append(acao)
            actions_listbox.insert(tk.END, f"Mouse clicado em {acao['posicao']} com o botão {acao['botao']}")
            time.sleep(delay)  # Delay entre os cliques do mouse

    # Iniciar capturas de eventos de teclado e mouse
    keyboard.hook(on_keyboard_event)
    with MouseListener(on_click=on_click) as listener:
        while not stop_gravacao:  # Verifica a flag para parar a gravação
            if keyboard.is_pressed('esc'):  # Detecta 'esc' para parar a gravação
                stop_gravacao = True
                break
            time.sleep(0.1)
        listener.stop()

    # Salva as ações gravadas em um arquivo
    with open('acoes_gravadas.pkl', 'wb') as f:
        pickle.dump(acoes, f)

    status_label.config(text="Gravação concluída.")
    parar_button.config(state=tk.DISABLED)  # Desativa o botão "Parar Gravação"
    reproduzir_button.config(state=tk.NORMAL)  # Ativa o botão "Reproduzir"
    gravar_button.config(state=tk.NORMAL)  # Ativa o botão "Gravar"
    keyboard.unhook(on_keyboard_event)  # Remove o hook de eventos de teclado

# Função para reproduzir as ações
def reproduzir_acao():
    try:
        with open('acoes_gravadas.pkl', 'rb') as f:
            acoes = pickle.load(f)

        status_label.config(text="Reproduzindo...")
        for acao in acoes:
            if acao['evento'] == 'teclado':
                if acao['tecla'] == 'Enter':
                    pyautogui.press('enter')  # Simula a tecla Enter
                    print("Tecla Enter pressionada")
                elif acao['tecla'] == 'space':
                    pyautogui.press('space')  # Simula a tecla de espaço
                    print("Tecla Espaço pressionada")
                elif acao['tecla'] == 'esc':
                    pyautogui.press('esc')  # Simula a tecla Esc
                    print("Tecla Esc pressionada")
                else:
                    keyboard.write(acao['tecla'])  # Simula a escrita da tecla
                    print(f"Tecla pressionada: {acao['tecla']}")
            elif acao['evento'] == 'teclado_atalho':
                if acao['comando'] == 'Ctrl+C':
                    pyautogui.hotkey('ctrl', 'c')  # Simula o atalho Ctrl+C
                    print("Atalho Ctrl+C executado")
                elif acao['comando'] == 'Ctrl+V':
                    pyautogui.hotkey('ctrl', 'v')  # Simula o atalho Ctrl+V
                    print("Atalho Ctrl+V executado")
            elif acao['evento'] == 'mouse_click':
                pyautogui.click(acao['posicao'][0], acao['posicao'][1])  # Executa o clique do mouse
                print(f"Clicando na posição: {acao['posicao']}")
                time.sleep(delay)  # Delay entre os cliques durante a reprodução
            elif acao['evento'] == 'sleep':
                time.sleep(acao['tempo'])  # Ação de sleep
                print(f"Esperando {acao['tempo']} segundos...")

            time.sleep(0.1)

        status_label.config(text="Reprodução concluída.")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Nenhuma gravação encontrada!")

# Função para iniciar a gravação em uma thread separada
def iniciar_gravacao():
    global stop_gravacao
    global delay
    stop_gravacao = False
    limpar_acoes()  # Limpa a lista de ações antes de iniciar uma nova gravação
    delay = float(delay_entry.get())  # Obtém o valor do delay inserido pelo usuário
    gravar_button.config(state=tk.DISABLED)  # Desativa o botão "Gravar"
    parar_button.config(state=tk.NORMAL)  # Ativa o botão "Parar Gravação"
    gravacao_thread = Thread(target=gravar_acao)
    gravacao_thread.start()

# Função para parar a gravação
def parar_gravacao():
    global stop_gravacao
    stop_gravacao = True  # Atualiza a flag para parar a gravação
    parar_button.config(state=tk.DISABLED)  # Desativa o botão "Parar Gravação"
    gravar_button.config(state=tk.NORMAL)  # Ativa o botão "Gravar"

# Função para adicionar uma nova ação manualmente
def adicionar_acao():
    acao_tipo = simpledialog.askstring("Tipo de Ação", "Digite o tipo da ação (mouse/teclado):")
    
    if acao_tipo == 'teclado':
        tecla = simpledialog.askstring("Tecla", "Digite a tecla a ser pressionada:")
        acao = {'evento': 'teclado', 'tecla': tecla}
        actions_listbox.insert(tk.END, f"Tecla pressionada: {tecla}")
    elif acao_tipo == 'mouse':
        x = simpledialog.askinteger("Posição X", "Digite a posição X:")
        y = simpledialog.askinteger("Posição Y", "Digite a posição Y:")
        acao = {'evento': 'mouse', 'posicao': (x, y)}
        actions_listbox.insert(tk.END, f"Mouse na posição: ({x}, {y})")
    else:
        messagebox.showerror("Erro", "Tipo de ação inválido.")
        return

    acoes.append(acao)  # Adiciona a nova ação à lista de ações gravadas

# Função para adicionar a ação de sleep
def adicionar_sleep():
    tempo_sleep = float(delay_entry.get())  # O tempo de sleep será o mesmo definido pelo usuário
    acao_sleep = {'evento': 'sleep', 'tempo': tempo_sleep}
    acoes.append(acao_sleep)
    actions_listbox.insert(tk.END, f"Sleep por {tempo_sleep} segundos")

    # Atualiza o arquivo com as novas ações
    with open('acoes_gravadas.pkl', 'wb') as f:
        pickle.dump(acoes, f)

# Função para remover uma ação específica da lista
def remover_acao():
    try:
        selected_index = actions_listbox.curselection()[0]  # Obtém o índice da ação selecionada
        actions_listbox.delete(selected_index)  # Remove a ação da listbox
        del acoes[selected_index]  # Remove a ação da lista interna
        
        # Atualiza o arquivo com as ações restantes
        with open('acoes_gravadas.pkl', 'wb') as f:
            pickle.dump(acoes, f)

        messagebox.showinfo("Sucesso", "Ação removida com sucesso!")
    except IndexError:
        messagebox.showerror("Erro", "Nenhuma ação selecionada para remover.")

# Função para mover a ação selecionada para cima
def mover_cima():
    try:
        selected_index = actions_listbox.curselection()[0]  # Obtém o índice da ação selecionada
        if selected_index > 0:
            # Move a ação para cima
            acao = acoes[selected_index]
            acoes[selected_index] = acoes[selected_index - 1]
            acoes[selected_index - 1] = acao
            actions_listbox.delete(selected_index)
            actions_listbox.insert(selected_index - 1, f"Tecla pressionada: {acao['tecla']}" if 'tecla' in acao else f"Mouse na posição: {acao['posicao']}" if 'posicao' in acao else f"Sleep por {acao['tempo']}" if 'tempo' in acao else "")
            
            # Atualiza o arquivo com as novas ações
            with open('acoes_gravadas.pkl', 'wb') as f:
                pickle.dump(acoes, f)
            
            # Re-seleciona o item que foi movido
            actions_listbox.selection_clear(0, tk.END)  # Limpa a seleção anterior
            actions_listbox.select_set(selected_index - 1)  # Seleciona o item movido
            
        else:
            messagebox.showerror("Erro", "A ação já está na primeira posição.")
    except IndexError:
        messagebox.showerror("Erro", "Nenhuma ação selecionada para mover.")

# Função para mover a ação selecionada para baixo
def mover_baixo():
    try:
        selected_index = actions_listbox.curselection()[0]  # Obtém o índice da ação selecionada
        if selected_index < len(acoes) - 1:
            # Move a ação para baixo
            acao = acoes[selected_index]
            acoes[selected_index] = acoes[selected_index + 1]
            acoes[selected_index + 1] = acao
            actions_listbox.delete(selected_index)
            actions_listbox.insert(selected_index + 1, f"Tecla pressionada: {acao['tecla']}" if 'tecla' in acao else f"Mouse na posição: {acao['posicao']}" if 'posicao' in acao else f"Sleep por {acao['tempo']}" if 'tempo' in acao else "")
            
            # Atualiza o arquivo com as novas ações
            with open('acoes_gravadas.pkl', 'wb') as f:
                pickle.dump(acoes, f)
            
            # Re-seleciona o item que foi movido
            actions_listbox.selection_clear(0, tk.END)  # Limpa a seleção anterior
            actions_listbox.select_set(selected_index + 1)  # Seleciona o item movido

        else:
            messagebox.showerror("Erro", "A ação já está na última posição.")
    except IndexError:
        messagebox.showerror("Erro", "Nenhuma ação selecionada para mover.")


# Função para limpar todas as ações gravadas
def limpar_acoes():
    global acoes
    acoes = []  # Limpa a lista de ações
    actions_listbox.delete(0, tk.END)  # Limpa a lista na interface

    # Atualiza o arquivo para refletir que não há mais ações
    with open('acoes_gravadas.pkl', 'wb') as f:
        pickle.dump(acoes, f)

# Função para exibir uma mensagem de ajuda
def exibir_ajuda():
    messagebox.showinfo("Ajuda", "Pressione 'esc' para parar a gravação.\nClique em 'Reproduzir' para executar as ações gravadas.")

# Configuração da janela principal
root = tk.Tk()
root.title("Gravação de Ações")
root.geometry("650x475")
root.resizable(False, False)

# Botões de gravação e reprodução
gravar_button = tk.Button(root, text="Gravar", width=20, command=iniciar_gravacao)
gravar_button.grid(row=0, column=0, pady=10, padx=5)

parar_button = tk.Button(root, text="Parar Gravação", width=20, command=parar_gravacao, state=tk.DISABLED)
parar_button.grid(row=0, column=1, pady=5, padx=5)

# Botãs para reproduzir ações
reproduzir_button = tk.Button(root, text="Reproduzir", width=20, command=reproduzir_acao, state=tk.DISABLED)
reproduzir_button.grid(row=1, column=0, pady=5, padx=5)

# Botão para carregar ações gravadas
carregar_button = tk.Button(root, text="Carregar Ações", width=20, command=carregar_acoes)
carregar_button.grid(row=1, column=1, pady=5, padx=5)

# Adicionando entrada para o delay
delay_label = tk.Label(root, text="Sleep entre Ações (segundos):")
delay_label.grid(row=2, column=0, pady=5, padx=5)

delay_entry = tk.Entry(root)
delay_entry.grid(row=2, column=1, pady=5, padx=5)
delay_entry.insert(tk.END, "2")  # Valor padrão de 1 segundo

adicionar_sleep_button = tk.Button(root, text="Adicionar Sleep", width=20, command=adicionar_sleep)
adicionar_sleep_button.grid(row=2, column=3, pady=5, padx=5)

# Criando um frame para colocar os botões de mover
move_frame = tk.Frame(root)
move_frame.grid(row=3, column=3, pady=5, padx=5)

# Botões de mover para cima e para baixo
mover_cima_button = tk.Button(move_frame, text="Subir Ação", width=20, command=mover_cima)
mover_cima_button.pack(pady=5)

mover_baixo_button = tk.Button(move_frame, text="Descer Ação", width=20, command=mover_baixo)
mover_baixo_button.pack(pady=5)

ajuda_button = tk.Button(move_frame, text="Ajuda", width=20, command=exibir_ajuda)
ajuda_button.pack(pady=5)

# Botões de limpar ações e remover ação específica
limpar_button = tk.Button(root, text="Limpar Ações", width=20, command=limpar_acoes)
limpar_button.grid(row=4, column=0, pady=5, padx=5)

remover_button = tk.Button(root, text="Remover Ação", width=20, command=remover_acao)
remover_button.grid(row=4, column=1, pady=5, padx=5)

# Label de status
status_label = tk.Label(root, text="Pronto", width=30)
status_label.grid(row=5, column=1, pady=10, padx=5)

# Lista de ações gravadas
actions_listbox = tk.Listbox(root, width=50, height=10)
actions_listbox.grid(row=3, column=0, columnspan=2, pady=10, padx=5)

# Iniciar o loop da interface gráfica
root.mainloop()
