function doisCaracteres(n) {
    if (n < 10) {
        return "0" + n;
    }
    return n;
}

function retornaDataAtual() {
    var dataAtual = new Date();
    var horaMinuto = doisCaracteres(dataAtual.getHours()) + ":" +
                     doisCaracteres(dataAtual.getMinutes());
    return "[" + horaMinuto + "] ";

}

function atualizaMensagens() {
    $.ajax({"url": "/atualizacao", success: function(data) {
        for (i = 0; i < data.mensagens.length; i++) {
            var origem = data.mensagens[i].origem;
            var mensagem = data.mensagens[i].mensagem;
            var elementoOrigem = $('#mensagens_' + origem + ' > .mensagens');
            var textoAtual = $(elementoOrigem).html();
            var dataAtual = retornaDataAtual();
            var novoTexto = dataAtual + mensagem + "<br>" + textoAtual;
            $(elementoOrigem).html(novoTexto);
        }
    }});
}

$(document).ready(function() {
    $('#texto').focus();
    atualizaMensagens();
    setInterval("atualizaMensagens()", 2000);

    $('#form_envia_msg').submit(function(e) {
        var textoDigitado = $('#texto').val();
        for (i = 0; i < textoDigitado.length; i++) {
            if (textoDigitado.charCodeAt(i) > 127) {
                alert('Você não pode enviar caracteres fora da tabela ASCII!');
                e.preventDefault();
                return;
            }
        }

        $('#texto').attr("disabled", "disabled");
        $('#destino').attr("disabled", "disabled");
        $('#enviar').attr("disabled", "disabled");
        $.ajax({type: 'POST', url: '/mensagem',
                data: {destino: $('#destino').val(), texto: $('#texto').val()},
                success: function(data) {
                    $('#texto').val('');
                    $('#texto').removeAttr("disabled");
                    $('#destino').removeAttr("disabled");
                    $('#enviar').removeAttr("disabled");
                    minhasMensagens = $('#mensagens_minhas > .mensagens');
                    textoAtual = minhasMensagens.html();
                    var mensagem = "Você disse a " + data.destino + ": " + data.mensagem;
                    var novoTexto = retornaDataAtual() + mensagem + "<br>" + textoAtual;
                    minhasMensagens.html(novoTexto);
                    $('#texto').focus();
                }
        });
        e.preventDefault();
    });
});
