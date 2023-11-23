import socket
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def string_para_binario(mensagem):
    return ''.join(format(ord(char), '08b') for char in mensagem)

def manchester_encode(data):
    
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
    string_signal = ''.join(encoded_signal)
    return string_signal


def pag_transmitor(ip):
    def make(ip, x):
        sinal_enviado(ip, x)
        binario = string_para_binario(x)
        cript = manchester_encode(binario)
        entry_binary.insert(0, binario)
        entry_cripto.insert(0, cript)
        plot_decoded_message(cript)

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
    msg_cripto = tk.Label(janela_transmitor, text="Mensagem criptografada:")
    entry_cripto = tk.Entry(janela_transmitor, width=20)
    


    botton_enviar = tk.Button(janela_transmitor, text="Enviar", width=15, command=lambda:make(ip, entry_insert.get()))

    insert_msg.pack(pady=10)
    entry_insert.pack(pady=10)
    msg_binary.pack(pady=10)
    entry_binary.pack(pady=10)
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
        # Envia dados para o cliente usando Manchester Diferencial
        conexao.send(mensagem_manchester.encode())
        # Fecha a conexão
        conexao.close()
        servidor.close()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
