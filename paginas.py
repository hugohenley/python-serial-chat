#!/usr/bin/env python
#coding: utf8

import json
import serial
from mensagem import cria_mensagem

ser = serial.Serial(port='/dev/ttyUSB1',
            baudrate = 9600,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_TWO,
            timeout = 0,
            xonxoff = True,
            rtscts = False)


interlocutores = {
        '00': 'João Marcos',
        '01': 'Hugo Henley',
        '10' :'Carlos Piffer',
        '11': 'Carol'
}
meu_endereco = '01'


def index(request):
    opcoes = []
    chats = []
    for endereco, nome in interlocutores.iteritems():
        if endereco != meu_endereco:
            chats.append('''<div class="chat" id="mensagens_%s"><b>%s</b>
                    diz:<br><div class="mensagens"></div></div>''' % (endereco, nome))
            opcoes.append('<option value="%s">%s</option>\n' % (endereco, nome))
    opcoes = ''.join(opcoes)
    chats = ''.join(chats)

    contents = '''<html>
  <head>
    <meta http-equiv="content-type" content="text/html;charset=utf8">
    <title>Chat com roteador</title>
    <link rel="stylesheet" type="text/css" href="/stylesheets/main.css">
    <script src="/scripts/jquery-1.6.4.min.js" type="text/javascript"></script>
    <script src="/scripts/chat.js" type="text/javascript"></script>
  </head>
  <body>
    %(chats)s
    <br>
    <div id="mensagens_minhas" class="chat"><b>Suas mensagens</b>: <br>
      <div class="mensagens"></div>
    </div>
    <br>
    <form method="POST" action="/mensagem" id="form_envia_msg">
      Texto: <input type="text" name="texto" id="texto">
      Destino: <select name="destino" id="destino">
%(opcoes)s
      </select>
      <input type="submit" value="Enviar" id="enviar">
    </form>
  </body>
</html>''' % {'chats': chats, 'opcoes': opcoes}

    return 200, contents


def envia_mensagem(request):
    if request.method != 'POST':
        return 405, 'Method not allowed!'
    if 'destino' not in request.postvars or 'texto' not in request.postvars:
        return 400, 'Bad request'

    destino = request.postvars['destino'][0]
    texto = request.postvars['texto'][0]
    mensagem = cria_mensagem(texto, meu_endereco, destino)
    for caractere in mensagem:
        ser.write(caractere)
    conteudo = json.dumps({'mensagem': texto,
                           'destino': interlocutores[destino]})
    return 200, conteudo, 'application/json;charset=utf-8'

def atualizacao(request):
    mensagem = []
    reading = True
    while reading:
        print "Lendo"
        c = ser.read(1)
        print c
        if not c:
            print "Nada enviado"
            reading = False
        else:
            print "Lendo o que foi enviado"
            mensagem.append(c)
            if ord(c) == 4:
                reading = False
    if mensagem:
        print "Chegou mensagem!"
        origem = ''
        cabecalho = mensagem[0]
        ord_mensagem = ord(mensagem[0])
        binario = bin(ord_mensagem)
        if len(binario) == 5:
            lista = list(binario)
            lista.insert(2,'0')
            binario = ''.join(lista)
        elif len(binario) == 4:
            lista = list(binario)
            lista.insert(2,'0')
            lista.insert(3,'0')
            binario = ''.join(lista)
        bit_origem_1 = ''.join(binario[2])
        bit_origem_2 = ''.join(binario[3])
        origem = bit_origem_1 + bit_origem_2
        
        msg = []
        for i in mensagem:
            indice = mensagem.index(i)
            if indice % 2 != 0:
                msg.append(i)
        msg.pop()
        msg_final = ''.join(msg)
        dados = {'mensagens': [{'origem': origem, 'mensagem': msg_final}]}
        conteudo = json.dumps(dados)
        return 200, conteudo, 'application/json;charset=utf-8'
    else:
        dados = {'mensagens': [{'origem': '01', 'mensagem': 'Sem mensagem'}]}
        conteudo = json.dumps(dados)
        return 200, conteudo, 'application/json;charset=utf-8'
