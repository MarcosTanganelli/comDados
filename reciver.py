import socket

def manchester_diferencial_para_bits(manchester):
    bits = ''
    ultimo_estado = '0'
    for i in range(0, len(manchester), 2):
        transicao = manchester[i:i+2]
        if transicao == '01' and ultimo_estado == '0':
            bits += '0'
        elif transicao == '10' and ultimo_estado == '0':
            bits += '1'
        elif transicao == '10' and ultimo_estado == '1':
            bits += '0'
        elif transicao == '01' and ultimo_estado == '1':
            bits += '1'
        ultimo_estado = bits[-1]
    return bits

def pag_reciver():
    print("Here")
# Configurações do cliente
host_servidor = '127.0.0.1'
porta_servidor = 12345

# Criação do socket do cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host_servidor, porta_servidor))

# Recebe dados do servidor
dados_recebidos = cliente.recv(1024).decode()
mensagem_bits = manchester_diferencial_para_bits(dados_recebidos)

print(f"Dados recebidos (Manchester Diferencial): {dados_recebidos}")
print(f"Mensagem decodificada (binário): {mensagem_bits}")

# Converte os bits de volta para a mensagem original
mensagem_decodificada = ''.join([chr(int(mensagem_bits[i:i+8], 2)) for i in range(0, len(mensagem_bits), 8)])

print(f"Mensagem decodificada: {mensagem_decodificada}")

# Fecha a conexão
cliente.close()
