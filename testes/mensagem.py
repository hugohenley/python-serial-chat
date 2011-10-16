#!/usr/bin/env python
#coding: utf8


import unittest
import sys
sys.path.insert(0, '..')
from mensagem import cria_cabecalho, cria_pacote, cria_mensagem


class TestCabecalho(unittest.TestCase):
    def test_caso_origem_nao_seja_string_deve_subir_ValueError(self):
        with self.assertRaises(TypeError) as context_manager:
            cria_cabecalho(origem=1, destino='10')
        exception = context_manager.exception
        self.assertEquals(str(exception), 'Origem deve ser uma string')


    def test_caso_destino_nao_seja_string_deve_subir_ValueError(self):
        with self.assertRaises(TypeError) as context_manager:
            cria_cabecalho(origem='10', destino=2)
        exception = context_manager.exception
        self.assertEquals(str(exception), 'Destino deve ser uma string')


    def test_a_string_de_origem_deve_conter_dois_caracteres_0_e_1(self):
        with self.assertRaises(ValueError) as context_manager:
            cria_cabecalho(origem='010101', destino='10')
        exception = context_manager.exception
        self.assertEquals(str(exception),
                          'Origem deve conter dois caracteres')


    def test_a_string_de_destino_deve_conter_dois_caracteres_0_e_1(self):
        with self.assertRaises(ValueError) as context_manager:
            cria_cabecalho(origem='01', destino='1010101')
        exception = context_manager.exception
        self.assertEquals(str(exception),
                          'Destino deve conter dois caracteres')


    def test_a_string_de_origem_deve_conter_binario(self):
        with self.assertRaises(ValueError) as context_manager:
            cria_cabecalho(origem='ab', destino='11')
        exception = context_manager.exception
        self.assertEquals(str(exception),
                          'Origem deve conter binario')


    def test_a_string_de_destino_deve_conter_binario(self):
        with self.assertRaises(ValueError) as context_manager:
            cria_cabecalho(origem='11', destino='qw')
        exception = context_manager.exception
        self.assertEquals(str(exception),
                          'Destino deve conter binario')


    def test_cria_cabecalho_com_origem_e_destino_01_para_10(self):
        cabecalho = cria_cabecalho(origem='01', destino='10')
        self.assertEqual(cabecalho, ['0', '0', '0', '0', '0', '1', '1', '0'])


    def test_cria_cabecalho_com_origem_e_destino_11_para_10(self):
        cabecalho = cria_cabecalho(origem='11', destino='10')
        self.assertEqual(cabecalho, ['0', '0', '0', '0', '1', '1', '1', '0'])


class TestPacote(unittest.TestCase):
    def test_deve_gerar_excecao_caso_caractere_nao_seja_ascii(self):
        with self.assertRaises(ValueError) as context_manager:
            cria_pacote(origem='10', destino='01', caractere='ç')
        excecao = context_manager.exception
        self.assertEqual(str(excecao), 'Caractere deve ser ASCII')


    def test_pacote_deve_conter_origem_destino_e_caractere_a(self):
        pacote = cria_pacote(origem='10', destino='01', caractere='a')
        self.assertEqual(pacote, chr(0b00001001) + 'a')


    def test_pacote_deve_conter_origem_destino_e_caractere_b(self):
        pacote = cria_pacote(origem='10', destino='01', caractere='b')
        self.assertEqual(pacote, chr(0b00001001) + 'b')


    def test_pacote_deve_refletir_origem_no_cabecalho_e_caractere_b(self):
        pacote = cria_pacote(origem='11', destino='01', caractere='b')
        self.assertEqual(pacote, chr(0b00001101) + 'b')


    def test_pacote_deve_refletir_destino_no_cabecalho_e_caractere_b(self):
        pacote = cria_pacote(origem='11', destino='00', caractere='b')
        self.assertEqual(pacote, chr(0b00001100) + 'b')


    def test_pacote_deve_aceitar_somente_um_caractere(self):
        with self.assertRaises(ValueError) as context_manager:
            cria_pacote(origem='11', destino='00', caractere='Oi')
        excecao = context_manager.exception
        self.assertEquals(str(excecao),
                          'Pacote deve conter apenas um caractere')


class TestMensagem(unittest.TestCase):
    def test_mensagem_um_caractere_retorna_2_pacotes(self):
        mensagem = cria_mensagem('A', origem='11', destino='01')
        cabecalho_esperado = chr(0b00001101)
        self.assertEqual(len(mensagem), 4)
        EOT = chr(4)
        self.assertEqual(mensagem[0], cabecalho_esperado)
        self.assertEqual(mensagem[1], 'A')
        self.assertEqual(mensagem[2], cabecalho_esperado)
        self.assertEqual(mensagem[3], EOT)


    def test_mensagem_com_dois_caracteres_retorna_3_pacotes(self):
        mensagem = cria_mensagem('Oi', origem='01', destino='10')
        cabecalho_esperado = chr(0b00000110)
        self.assertEqual(len(mensagem), 6)
        EOT = chr(4)
        self.assertEqual(mensagem[0], cabecalho_esperado)
        self.assertEqual(mensagem[1], 'O')
        self.assertEqual(mensagem[2], cabecalho_esperado)
        self.assertEqual(mensagem[3], 'i')
        self.assertEqual(mensagem[4], cabecalho_esperado)
        self.assertEqual(mensagem[5], EOT)



unittest.main()
