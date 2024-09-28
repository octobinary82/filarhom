# -*- coding: utf-8 -*-

from g4f.client import Client
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_gpt_response(query):
  client = Client()
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": query}])

  return response.choices[0].message.content


class SimpleHandler(BaseHTTPRequestHandler):
    # Método que lida com requisições POST
    def do_POST(self):
        # Verificar o caminho solicitado
        if self.path == '/response':
            # Lê o comprimento do conteúdo (corpo da requisição)
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                # Lê o corpo da requisição
                body = self.rfile.read(content_length).decode('utf-8')
            else:
                body = 'No body sent'

            # Enviar a resposta
            self.send_response(200)  # Código de status 200: OK
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # Aqui você pode processar o corpo e gerar uma resposta personalizada
            response = f"Body received: {body}"
            print(response)  # Exibir o corpo recebido no console

            # Exemplo: Simulação de resposta (altere 'get_gpt_response' conforme necessário)
            self.wfile.write(get_gpt_response(body).encode('utf-8'))
        else:
            self.send_response(404)  # Retorna 404 se o endpoint não for '/response'
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8092):
    server_address = ('', port)  # Configura o servidor para rodar em localhost e a porta fornecida
    httpd = server_class(server_address, handler_class)
    print(f'Servidor rodando na porta {port}...')
    httpd.serve_forever()  # Mantém o servidor rodando

run()
