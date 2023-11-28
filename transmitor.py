import socket
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

def string_para_binario(mensagem):
    return ''.join(format(ord(char), '08b') for char in mensagem)

def manchester_encode(data):
    
    if isinstance(data, str):
        data = [int(bit) for bit in data]

    encoded_signal = ['1']

    for bit in data:
        last = encoded_signal[-1]
        if bit == 0:
            if last == '1':
                encoded_signal.append('0')  
                encoded_signal.append('1')  
            else :
                encoded_signal.append('1')
                encoded_signal.append('0')

        else:
            if last == '1':
                encoded_signal.append('1') 
                encoded_signal.append('0')  

            else:
                encoded_signal.append('0')
                encoded_signal.append('1')

    encoded_signal.pop(0)
    result_string = ''.join(map(str, encoded_signal))
    return result_string

def criptografar(chave, sinal_binario):
    binary = sinal_binario.encode('utf-8')
    # Gera um vetor de inicialização (IV) aleatório
    iv = os.urandom(16)

    # Cria um objeto de cifra AES com a chave e o modo CBC
    cipher = Cipher(algorithms.AES(chave), modes.CFB(iv), backend=default_backend())

    # Cria um objeto de enchimento PKCS7
    padder = padding.PKCS7(128).padder()

    # Aplica o enchimento aos dados
    dados_encriptados = cipher.encryptor().update(padder.update(binary) + padder.finalize())

    # Retorna o IV concatenado com os dados criptografados
    return iv + dados_encriptados


def pag_transmitor(ip):
    def make(ip, x):
        sinal_enviado(ip, x)
        binario = string_para_binario(x)
        cod_linha = manchester_encode(binario)
        cript = criptografar(b'0111101010101011', cod_linha)
        entry_binary.delete(0, tk.END)
        entry_binary.insert(0, binario)
        msg_codlinha.delete(0, tk.END)
        msg_codlinha.insert(0, cod_linha)
        entry_cripto.delete(0, tk.END)
        entry_cripto.insert(0, cript)
        plot_decoded_message(cod_linha)

    def plot_decoded_message(decoded_message):
        # Criar uma janela para o gráfico
        # plot_window = tk.Toplevel()
        # plot_window.title("Decoded Message Plot")

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
        plot.set_title("Decoded Message Plot")
        plot.set_xlabel("Index")
        plot.set_ylabel("ASCII Value")

        # Incorporar a figura no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=janela_transmitor)
        widget_canvas = canvas.get_tk_widget()
        widget_canvas.pack(expand=True, fill=tk.BOTH)


    janela_transmitor = tk.Toplevel()
    janela_transmitor.title("Transmitor")
    janela_transmitor.geometry("600x600")
    insert_msg = tk.Label(janela_transmitor, text="Insira a Mensagem:")
    entry_insert = tk.Entry(janela_transmitor, width=20)
    msg_binary = tk.Label(janela_transmitor, text="Mensagem em binário:")
    entry_binary = tk.Entry(janela_transmitor, width=20)
    label_codlinha = tk.Label(janela_transmitor, text="Codigo de linha:")
    msg_codlinha = tk.Entry(janela_transmitor, width=20)
    msg_cripto = tk.Label(janela_transmitor, text="Mensagem criptografada:")
    entry_cripto = tk.Entry(janela_transmitor, width=20)
    


    botton_enviar = tk.Button(janela_transmitor, text="Enviar", width=15, command=lambda:make(ip, entry_insert.get()))

    insert_msg.pack(pady=10)
    entry_insert.pack(pady=10)
    msg_binary.pack(pady=10)
    entry_binary.pack(pady=10)
    label_codlinha.pack(pady=10)
    msg_codlinha.pack(pady= 10)
    msg_cripto.pack(pady=10)
    entry_cripto.pack(pady=10)
    botton_enviar.pack(pady=10)



def sinal_enviado(ip, txt):
    try:
        # Configurações do servidor
        host = ip
        porta = 12345
        # Criação do socket do servidor
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((host, porta))
        servidor.listen()
        print(f"Servidor ouvindo em {host}:{porta}")
        # Aguarda a conexão do cliente
        conexao, endereco_cliente = servidor.accept()
        print(f"Conexão estabelecida com {endereco_cliente}")
        # Converte a mensagem para binário
        mensagem_binaria = string_para_binario(txt)
        # Aplica a codificação Manchester Diferencial
        mensagem_manchester = manchester_encode(mensagem_binaria)
        msg_criptografada = criptografar(b'0111101010101011', mensagem_manchester)
        conexao.send(msg_criptografada.encode())
        # Fecha a conexão
        conexao.close()
        servidor.close()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
