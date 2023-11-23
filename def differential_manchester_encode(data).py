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
    return encoded_signal

def manchester_decode(data):
    if isinstance(data, str):
        data = [int(bit) for bit in data]
    result = []
    data.insert(0, '1')
    for i in range(0, len(data) - 1, 2):
        result.append('1') if data[i] == data[i + 1] else result.append('0')

    return result









# Exemplo de uso
data_bits = '0110111101101001'
# 10011001100110011001100110011001 cript
print(data_bits)
manchester_encoded_signal = manchester_encode(data_bits)
manchester_decoded_signal = manchester_decode(manchester_encoded_signal)

print("Manchester encoding:", manchester_encoded_signal)
print("Manchester encoding:", manchester_decoded_signal)

