

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


def descriptografa(passo, criptografado):
    num = True
    texto_original = ''
    vec = mapeia(passo)
    i = 0  # Inicializa o índice fora do loop para controlar manualmente
    letra = ''
    while i < len(criptografado):
        if num:
            tmp = criptografado[i:i+3]
            for j, item in enumerate(vec):
                if item['map'] == tmp:
                    letra = item['type']
                    break
            i += 3
        else:
            print(ord(criptografado[i]))
            for j, item in enumerate(vec):
                if item['type'] == str(criptografado[i]):
                    for k, temp in enumerate(vec):
                        if temp['map'] == str(j):
                            letra = chr(k)
                    break
            i += 1
        texto_original += letra
        num = not num  # Inverte o valor de num

    return texto_original


mensagem_original = "oiyu"
chave = 3

mensagem_cifrada = criptografar(chave, mensagem_original)
print("Mensagem cifrada:", mensagem_cifrada)

mensagem_decifrada = descriptografa(chave, mensagem_cifrada)
print("Mensagem decifrada:", mensagem_decifrada)

