import tkinter as tk
import socket
import threading
import time

def manchester_decode(data):
    # Verifica se a entrada é uma string e a converte em uma lista se necessário
    if isinstance(data, str):
        data = [int(bit) for bit in data]


    result = []
    data.insert(0, '1')

    for i in range(0, len(data) - 1, 2):
        result.append('1') if data[i] == data[i + 1] else result.append('0')

    # Convertendo a lista resultante de volta para uma string
    result_string = ''.join(result)
    return result_string

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

def sinal_descriptografado(sinal):
    mensagem_bits = manchester_decode(sinal)
    print(f"Mensagem decodificada (binário): {mensagem_bits}")
    return mensagem_bits

def sinal_txt(bits):
    mensagem_decodificada = ''.join([chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)])
    print(f"Mensagem decodificada: {mensagem_decodificada}")
    return mensagem_decodificada

def pag_receiver(ip):
    def preencher_lacunas(sinal):
        # Preencher as entradas com o sinal recebido
        entry_cripto.config(state="normal")
        entry_cripto.delete(0, tk.END)
        entry_cripto.insert(0, sinal)

        bits = sinal_descriptografado(sinal)
        entry_binary.config(state="normal")
        entry_binary.delete(0, tk.END)
        entry_binary.insert(0, bits)

        texto_decodificado = sinal_txt(bits)
        entry_txt.config(state="normal")
        entry_txt.delete(0, tk.END)
        entry_txt.insert(0, texto_decodificado)

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
    janela_receiver.resizable(False, False)
    janela_receiver.geometry("300x300")

    msg_cripto = tk.Label(janela_receiver, text="Mensagem criptografada:")
    entry_cripto = tk.Entry(janela_receiver, width=20)

    msg_binary = tk.Label(janela_receiver, text="Mensagem em binário:")
    entry_binary = tk.Entry(janela_receiver, width=20)

    msg_txt = tk.Label(janela_receiver, text="Mensagem descriptografada:")
    entry_txt = tk.Entry(janela_receiver, width=20)

    msg_cripto.pack(pady=10)
    entry_cripto.pack(pady=10)
    msg_binary.pack(pady=10)
    entry_binary.pack(pady=10)
    msg_txt.pack(pady=10)
    entry_txt.pack(pady=10)

    # Inicia uma thread para verificar continuamente o sinal
    thread_verificar_sinal = threading.Thread(target=verificar_sinal, daemon=True)
    thread_verificar_sinal.start()

    janela_receiver.mainloop()

# Resto do código permanece o mesmo...
