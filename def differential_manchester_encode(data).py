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







# Exemplo de uso
# data_bits = '10011001100110011001100110011001'
# 
txt = 'oi'
data_bits = string_para_binario(txt)
machester = manchester_encode(data_bits)
binario = manchester_decode(machester)
txt = sinal_txt(binario)

print("txt: ", txt)
print("///////////////////////\n binario:", data_bits)
print("///////////////////////\nManchester :", machester)



print("///////////////////////\nbinario:", binario)
print("///////////////////////\ntxt:", txt)


