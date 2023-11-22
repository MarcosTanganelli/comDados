import socket
import tkinter as tk

def string_para_binario(mensagem):
    return ''.join(format(ord(char), '08b') for char in mensagem)

def manchester_diferencial(bits):
    manchester = ''
    ultimo_estado = '0'
    for bit in bits:
        if bit == '0':
            manchester += '01' if ultimo_estado == '0' else '10'
        else:
            manchester += '10' if ultimo_estado == '0' else '01'
        ultimo_estado = bit
    return manchester


def pag_transmitor(ip):
    janela_transmitor = tk.Toplevel()
    janela_transmitor.title("Transmitor")
    janela_transmitor.resizable(False, False)
    janela_transmitor.grab_set()
    janela_transmitor.geometry("300x300")
    insert_msg = tk.Label(janela_transmitor, text="Insira a Mensagem:")
    entry_insert = tk.Entry(janela_transmitor, width=20)
    msg_binary = tk.Label(janela_transmitor, text="Mensagem em binário:")
    entry_binary = tk.Entry(janela_transmitor, width=20, state="disabled")
    msg_cripto = tk.Label(janela_transmitor, text="Mensagem criptografada:")
    entry_cripto = tk.Entry(janela_transmitor, width=20, state="disabled")
    botton_enviar = tk.Button(janela_transmitor, text="Enviar", width=15, command=lambda:sinal_enviado(ip,entry_insert.get()))

    insert_msg.pack(pady=10)
    entry_insert.pack(pady=10)
    msg_binary.pack(pady=10)
    entry_binary.pack(pady=10)
    msg_cripto.pack(pady=10)
    entry_cripto.pack(pady=10)
    botton_enviar.pack(pady=10)



def sinal_enviado(ip, txt):
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
    mensagem_manchester = manchester_diferencial(mensagem_binaria)
    # Envia dados para o cliente usando Manchester Diferencial
    conexao.send(mensagem_manchester.encode())
    # Fecha a conexão
    conexao.close()
    servidor.close()
