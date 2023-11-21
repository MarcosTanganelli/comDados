import socket

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

def pag_transmitor():
    print("here 2")

# Configurações do servidor
host = '127.0.0.1'
porta = 12345

# Criação do socket do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, porta))
servidor.listen()

print(f"Servidor ouvindo em {host}:{porta}")

# Aguarda a conexão do cliente
conexao, endereco_cliente = servidor.accept()
print(f"Conexão estabelecida com {endereco_cliente}")

# Mensagem original em formato de string
mensagem_original = "Hello, World!"

# Converte a mensagem para binário
mensagem_binaria = string_para_binario(mensagem_original)

# Aplica a codificação Manchester Diferencial
mensagem_manchester = manchester_diferencial(mensagem_binaria)

# Envia dados para o cliente usando Manchester Diferencial
conexao.send(mensagem_manchester.encode())

# Fecha a conexão
conexao.close()
servidor.close()
