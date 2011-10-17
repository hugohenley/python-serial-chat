
import serial

ser = serial.Serial(port='/dev/ttyUSB0',
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_TWO,
            timeout = None,
            xonxoff = True,
            rtscts = False)


def read_serial():
    mensagem = []
    reading = True
    while reading:
        print "aqui"
        c = ser.read(1)
        print c
        print "aqui 3"
        mensagem.append(c)
        if ord(c) == 4:
            reading = False
    if mensagem:
        print "aqui 4"
        origem = ''
        cabecalho = mensagem[0]
        bin = bin(ord(mensagem[0]))
        if len(bin) == 5:
            lista = list(bin)
            lista.insert(2,'0')
            bin = ''.join(lista)
        elif len(bin) == 4:
            lista = list(bin)
            lista.insert(2,'0')
            lista.insert(3,'0')
            bin = ''.join(lista)
        bit_origem_1 = ''.join(bin[2])
        bit_origem_2 = ''.join(bin[3])
        origem = bit_origem_1 + bit_origem_2
        
        msg = []
        for i in mensagem:
            indice = mensagem.index(i)
            if indice % 2 != 0:
                msg.append(i)
        msg.pop()
        msg_final = ''.join(msg)
    reading = True
    origem_msg = []
    origem_msg.append(origem)
    origem_msg.append(msg_final)
    return origem_msg

