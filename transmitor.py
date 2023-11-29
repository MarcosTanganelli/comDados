import socket
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def criptografar(passo, texto):
    num = True
    vec = mapeia(passo)
    crip = ''
    for char in texto:
        for item in vec:
            if item['type'] == char:
                letra = item['map']
                if num:
                    num = False
                    crip += str(letra)
                else:
                    num = True
                    letra = chr(int(letra))
                    crip += letra
                break
    return crip


def pag_transmitor(ip):
    def make(ip, texto):
        criptografia = criptografar(3, texto)
        binario   = string_para_binario(criptografia)
        cod_linha = manchester_encode(binario)
        sinal_enviado(ip, cod_linha)

        entry_cripto.delete(0, tk.END)
        entry_cripto.insert(0, criptografia)
        entry_binary.delete(0, tk.END)
        entry_binary.insert(0, binario)
        entry_codlinha.delete(0, tk.END)
        entry_codlinha.insert(0, cod_linha)

        plot_decoded_message(cod_linha, janela_transmitor)

    def plot_decoded_message(decoded_message, frame):
        if hasattr(frame, 'widget_canvas') and frame.widget_canvas.winfo_exists():
            frame.widget_canvas.destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)

        square_wave = []
        for val in decoded_message:
            square_wave.extend([val, val])

        plot.plot(square_wave, drawstyle='steps-post')

        plot.set_title("Codigo de linha")


        canvas = FigureCanvasTkAgg(fig, master=frame)
        frame.widget_canvas = canvas.get_tk_widget()
        frame.widget_canvas.pack(expand=True, fill=tk.BOTH)


    janela_transmitor = tk.Toplevel()
    janela_transmitor.title("Transmitor")
    janela_transmitor.geometry("600x600")
    insert_msg      = tk.Label(janela_transmitor, text="Insira a Mensagem:")
    entry_insert    = tk.Entry(janela_transmitor, width=20)
    msg_binary      = tk.Label(janela_transmitor, text="Mensagem em binário:")
    entry_binary    = tk.Entry(janela_transmitor, width=20)
    label_codlinha  = tk.Label(janela_transmitor, text="Codigo de linha:")
    entry_codlinha    = tk.Entry(janela_transmitor, width=20)
    msg_cripto      = tk.Label(janela_transmitor, text="Mensagem criptografada:")
    entry_cripto    = tk.Entry(janela_transmitor, width=20)
    botton_enviar   = tk.Button(janela_transmitor, text="Enviar", width=15, command=lambda:make(ip, entry_insert.get()))

    insert_msg.pack(pady=10)
    entry_insert.pack(pady=10)
    msg_cripto.pack(pady=10)
    entry_cripto.pack(pady=10)
    msg_binary.pack(pady=10)
    entry_binary.pack(pady=10)
    label_codlinha.pack(pady=10)
    entry_codlinha.pack(pady= 10)
    botton_enviar.pack(pady=10)



def sinal_enviado(ip, codlinha):
    try:
        binary = codlinha.encode()
        host = ip
        porta = 12345
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((host, porta))
        servidor.listen()
        print(f"Servidor ouvindo em {host}:{porta}")
        conexao, endereco_cliente = servidor.accept()
        print(f"Conexão estabelecida com {endereco_cliente}")
        conexao.send(binary)
        conexao.close()
        servidor.close()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
