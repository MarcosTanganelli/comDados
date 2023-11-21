import tkinter as tk
import reciver
import transmitor

# Criar janela principal
janela = tk.Tk()
janela.title("Menu")

# Definir funções para os botões
botao1 = tk.Button(janela, text="Reciver", command=lambda:reciver.pag_reciver())
botao2 = tk.Button(janela, text="Transmitor", command=lambda:transmitor.pag_transmitor())

# Organizar os botões na janela
botao1.pack(pady=10)
botao2.pack(pady=10)

# Iniciar o loop principal da interface gráfica
janela.mainloop()
