from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
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



def string_para_binario(mensagem):
    return ''.join(format(ord(char), '08b') for char in mensagem)

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



def criptografar(chave, sinal_binario):
    # Gera um vetor de inicialização (IV) aleatório
    iv = os.urandom(16)

    # Cria um objeto de cifra AES com a chave e o modo CFB
    cipher = Cipher(algorithms.AES(chave), modes.CFB(iv), backend=default_backend())

    # Criptografa os dados
    dados_encriptados = cipher.encryptor().update(sinal_binario) + cipher.encryptor().finalize()

    # Retorna o IV concatenado com os dados criptografados
    return iv + dados_encriptados

def descriptografar(chave, sinal_criptografado):
    # Extrai o IV do sinal criptografado
    iv = sinal_criptografado[:16]

    # Cria um objeto de cifra AES com a chave e o modo CFB
    cipher = Cipher(algorithms.AES(chave), modes.CFB(iv), backend=default_backend())

    # Descriptografa os dados
    dados_descriptografados = cipher.decryptor().update(sinal_criptografado[16:]) + cipher.decryptor().finalize()

    return dados_descriptografados

# Exemplo de uso:
chave = '0111101010101011'  # Chave AES de 128, 192 ou 256 bits
chave =  chave.encode()
sinal_original = "teste"  # Substitua isso pelo seu sinal binário

# Criptografa o sinal
sinal_criptografado = criptografar(chave, sinal_original)
print("Sinal criptografado:", urlsafe_b64encode(sinal_criptografado))

# Descriptografa o sinal
sinal_descriptografado = descriptografar(chave, sinal_criptografado)
print("Sinal descriptografado:", sinal_descriptografado)

