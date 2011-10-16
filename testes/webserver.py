import unittest
import urllib


BASE_URL = 'http://localhost:8001'

class TestWebServer(unittest.TestCase):
    def test_get_na_mensagem_deve_retornar_status_code_405(self):
        f = urllib.urlopen(BASE_URL + '/mensagem')
        self.assertEquals(f.getcode(), 405)
        self.assertEquals(f.read(), 'Method not allowed!')


    def test_post_sem_destino_e_texto_deve_retornar_status_code_400(self):
        params = urllib.urlencode({'asd': '123'})
        f = urllib.urlopen(BASE_URL + '/mensagem', params)
        self.assertEquals(f.getcode(), 400)
        self.assertEquals(f.read(), 'Bad request')


    def test_post_sem_destino_com_texto_deve_retornar_status_code_400(self):
        params = urllib.urlencode({'texto': '123'})
        f = urllib.urlopen(BASE_URL + '/mensagem', params)
        self.assertEquals(f.getcode(), 400)
        self.assertEquals(f.read(), 'Bad request')


    def test_post_com_destino_sem_texto_deve_retornar_status_code_400(self):
        params = urllib.urlencode({'destino': '123'})
        f = urllib.urlopen(BASE_URL + '/mensagem', params)
        self.assertEquals(f.getcode(), 400)
        self.assertEquals(f.read(), 'Bad request')


unittest.main()
