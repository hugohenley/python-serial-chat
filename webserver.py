#!/usr/bin/env python
#coding: utf8

from httpy import MicroFramework
from mensagem import cria_mensagem
import paginas


port = 3000
url_mapping = {'/': paginas.index,
               '/mensagem': paginas.envia_mensagem,
               '/scripts/jquery-1.6.4.min.js': 'static/jquery-1.6.4.min.js',
               '/scripts/chat.js': 'static/chat.js',
               '/stylesheets/main.css': 'static/main.css',
               '/atualizacao': paginas.atualizacao,
}
my_server = MicroFramework(url_mapping, port)
print 'Iniciando servidor na porta %d...' % port
my_server.serve()
