def cria_cabecalho(origem, destino):
    cabecalho = ['0', '0', '0', '0']
    binario = ['0', '1']
    if not isinstance(origem, str):
        raise TypeError, 'Origem deve ser uma string'
    elif not isinstance(destino, str):
        raise TypeError, 'Destino deve ser uma string'
    elif len(origem) != 2:
        raise ValueError, 'Origem deve conter dois caracteres'
    elif len(destino) != 2:
        raise ValueError, 'Destino deve conter dois caracteres'
    elif origem[0] not in binario or origem[1] not in binario:
        raise ValueError, 'Origem deve conter binario'
    elif destino[0] not in binario or destino[1] not in binario:
        raise ValueError, 'Destino deve conter binario'

    cabecalho.extend(list(origem))
    cabecalho.extend(list(destino))
    return cabecalho


def cria_pacote(origem, destino, caractere):
    try:
        caractere = caractere.decode('ascii')
    except ValueError:
        raise ValueError, 'Caractere deve ser ASCII'
    if len(caractere) != 1:
        raise ValueError, 'Pacote deve conter apenas um caractere'
    cabecalho = cria_cabecalho(origem, destino)
    cabecalho_bin = 0
    cabecalho.reverse()
    for i, j in enumerate(cabecalho):
        cabecalho_bin += int(j) * (2 ** i)

    return chr(cabecalho_bin) + caractere


def cria_mensagem(texto, origem, destino):
    pacotes = []
    for caractere in texto:
        pacotes.append(cria_pacote(origem, destino, caractere))
    pacotes.append(cria_pacote(origem, destino, chr(4)))
    return ''.join(pacotes)
    
