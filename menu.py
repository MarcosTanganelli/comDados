import tkinter as tk
import reciver
import transmitor
# Criar janela principal
janela = tk.Tk()
janela.title("Menu")
janela.geometry("200x200")
valor_inicial = "10.181.12.106"
# Criação dos elementos da interface gráfica
label_ip = tk.Label(text="IP do transmissor:")
entry_ip = tk.Entry(width=20)
entry_ip.insert(0, valor_inicial)
botao1 = tk.Button(janela, text="Receiver", width=15, command=lambda:reciver.pag_receiver(entry_ip.get()))
botao2 = tk.Button(janela, text="Transmissor", width=15, command=lambda:transmitor.pag_transmitor(entry_ip.get()))

# Organização dos elementos na janela
label_ip.pack(pady=10)
entry_ip.pack(pady=10)
botao1.pack(pady=10)
botao2.pack(pady=10)


# Iniciar o loop principal da interface gráfica
janela.mainloop()
