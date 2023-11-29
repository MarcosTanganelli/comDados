import tkinter as tk
import socket
import threading
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def mapeia(passo):
    vec = []
    copy_vec = []

    for i in range(256):
        vec.append({'type': chr(i)})
        copy_vec.append(i)

    while not all(x == -1 for x in copy_vec):
        if i + passo >= 256:
            i -= 256
        
        tmp = copy_vec[i + passo]
        char = f'{tmp:03d}'
        if char != vec[i]['type']:
            vec[i]['map'] = char

        copy_vec[i + passo] = -1
        i += passo

    return vec

def descriptografa(passo, criptografado):
    num = True
    texto_original = ''
    vec = mapeia(passo)
    i = 0  # Inicializa o índice fora do loop para controlar manualmente
    letra = ''
    while i < len(criptografado):
        if num:
            tmp = criptografado[i:i+3]
            for j, item in enumerate(vec):
                if item['map'] == tmp:
                    letra = item['type']
                    break
            i += 3
        else:
            print(ord(criptografado[i]))
            for j, item in enumerate(vec):
                if item['type'] == str(criptografado[i]):
                    for k, temp in enumerate(vec):
                        if temp['map'] == str(j):
                            letra = chr(k)
                    break
            i += 1
        texto_original += letra
        num = not num  # Inverte o valor de num

    return texto_original

def manchester_decode(data):
    if isinstance(data, str):
        data = [int(bit) for bit in data]
    result = []
    data.insert(0, '1')
    for i in range(0, len(data) - 1, 2):
        result.append('1') if data[i] == data[i + 1] else result.append('0')

    result_string = ''.join(map(str, result))
    return result_string


def sinal_txt(binario):
    try:
        # Dividindo a string binária em partes de 8 bits
        bytes_binarios = [binario[i:i+8] for i in range(0, len(binario), 8)]

        # Convertendo cada byte para um número inteiro e, em seguida, para um caractere ASCII
        texto = ''.join([chr(int(byte, 2)) for byte in bytes_binarios])

        # Retornando a string resultante
        return texto
    except ValueError:
        # Se houver um erro ao converter, retorna uma mensagem de erro
        return "Erro: A entrada não é uma string binária válida."

def sinal_recebido(ip):
    # Configurações do cliente
    host_servidor = ip
    porta_servidor = 12345
    # Criação do socket do cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host_servidor, porta_servidor))
    # Recebe dados do servidor
    dados_recebidos = cliente.recv(1024).decode()
    print(f"Dados recebidos (Manchester Diferencial): {dados_recebidos}")
    cliente.close()
    return dados_recebidos

def sinal_decodlinha(sinal):
    mensagem_bits = manchester_decode(sinal)
    print(f"Mensagem decodificada (binário): {mensagem_bits}")
    return mensagem_bits





def pag_receiver(ip):
    def plot_decoded_message(decoded_message, frame):
        # Se existir um widget de gráfico anterior, destrua-o
        if hasattr(frame, 'widget_canvas') and frame.widget_canvas.winfo_exists():
            frame.widget_canvas.destroy()

        # Criar uma figura do Matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)

        # Criar uma onda quadrada alternando rapidamente entre 0 e 1
        square_wave = []
        for val in decoded_message:
            square_wave.extend([val, val])

        # Plotar a onda quadrada
        plot.plot(square_wave, drawstyle='steps-post')

        # Adicionar rótulos
        plot.set_title("Codigo de linha")


        # Incorporar a figura no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        frame.widget_canvas = canvas.get_tk_widget()
        frame.widget_canvas.pack(expand=True, fill=tk.BOTH)
            
    def preencher_lacunas(codlinha):
        # Preencher as entradas com o sinal recebido
        decode_linha = sinal_decodlinha(codlinha)
        criptografado = sinal_txt(decode_linha)
        msg = descriptografa(3, criptografado)

        entry_codlinha.config(state="normal")
        entry_codlinha.delete(0, tk.END)
        entry_codlinha.insert(0, codlinha)

        entry_binario.config(state="normal")
        entry_binario.delete(0, tk.END)
        entry_binario.insert(0, decode_linha)

        entry_cripto.config(state="normal")
        entry_cripto.delete(0, tk.END)
        entry_cripto.insert(0, criptografado)

        entry_decripto.config(state="normal")
        entry_decripto.delete(0, tk.END)
        entry_decripto.insert(0, msg)
        
        plot_decoded_message(codlinha, janela_receiver)
        

    def verificar_sinal():
        while True:
            try:
                sinal = sinal_recebido(ip)
                janela_receiver.after(0, preencher_lacunas, sinal)
                time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente
            except Exception as e:
                print(f"Erro ao verificar sinal: {e}")
                time.sleep(1)  # Aguarda 1 segundo em caso de erro

    janela_receiver = tk.Toplevel()
    janela_receiver.title("Receiver")
    janela_receiver.geometry("500x500")

    msg_cripto = tk.Label(janela_receiver, text="Mensagem criptografada:")
    entry_cripto = tk.Entry(janela_receiver, width=20)

    msg_decripto = tk.Label(janela_receiver, text="Mensagem:")
    entry_decripto = tk.Entry(janela_receiver, width=20)

    msg_codlinha = tk.Label(janela_receiver, text="Mensagem em codigo de linha:")
    entry_codlinha = tk.Entry(janela_receiver, width=20)

    msg_binario = tk.Label(janela_receiver, text="Mensagem em binario:")
    entry_binario = tk.Entry(janela_receiver, width=20)


    msg_codlinha.pack(pady=10)
    entry_codlinha.pack(pady=10)
    msg_binario.pack(pady=10)
    entry_binario.pack(pady=10)
    msg_cripto.pack(pady=10)
    entry_cripto.pack(pady=10)
    msg_decripto.pack(pady=10)
    entry_decripto.pack(pady=10)


    # Inicia uma thread para verificar continuamente o sinal
    thread_verificar_sinal = threading.Thread(target=verificar_sinal, daemon=True)
    thread_verificar_sinal.start()

    janela_receiver.mainloop()
