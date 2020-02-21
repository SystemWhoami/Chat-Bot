import sqlite3
import re
import random


class ChatterBot:


""" ChatterBot simples usando SQLite para armazenar conhecimento e
Regex(Expressões regulares) para identificar entrada para calculos. """


def __init__(self):


""" Construtor. """
self.bd_mensagens = sqlite3.connect('bd_mensagens.db')

self.prompt_user = ": "
self.prompt_bot = "> "

self.lista_mensagens = self.bd_mensagens.\
    execute("SELECT chave, valor FROM mensagens ORDER BY chave").fetchall()

self.interagir()


def interagir(self) -> None:


""" Função de interação.
:return: None. """
while 1:
try:
msg = input(self.prompt_user).lower()

padrao = r'^[0-9]+\.?[0-9]*([\+\-\/%]|[\*]{1,2})[0-9]+\.?[0-9]*$'

if re.search(padrao, msg):
print(self.prompt_bot + str(eval(msg)))
else:
if msg == 'ls':
temp = ""
print(self.prompt_bot +
      "Listagem de comandos disponíveis:")
for linha in self.lista_mensagens:
if linha[0] != temp:
print(self.prompt_bot + linha[0])
temp = linha[0]
elif msg in ('help', 'ajuda'):
print(self.prompt_bot +
      'Digite ls para listar os comandos disponíveis e informe um deles ou\n'
      '> Informe um calculo(ex: 1+1) ou\n'
      '> Informe =pergunta_existente para cadastrar nova resposta(use REGEX para melhor'
      'performance, ex: ol[aá])')
else:
resposta = []

if re.search(r'^=.+', msg):
msg = msg[1:]

for item in self.lista_mensagens:
if re.search(item[0], msg):
msg = item[0]
break
else:
for item in self.lista_mensagens:
if re.search(item[0], msg):
resposta.append(item[1])

if resposta:
if resposta[0] == "quit":
break
else:
random.shuffle(resposta)
print("%s%s" % (self.prompt_bot, resposta[0]))
else:
print("{0}Não sei como interagir\n{1}Deseja cadastrar a interação[S/n]: ".format(
    self.prompt_bot, self.prompt_bot), end="")
confirmacao = input("").lower()

if confirmacao == "s":
try:
self.bd_mensagens.execute("INSERT INTO mensagens(chave, valor)"
                          "VALUES('%s', '%s')" %
                          (msg, input("Resposta para '%s': " % msg)))
self.bd_mensagens.commit()

self.lista_mensagens = self.bd_mensagens.execute(
    "SELECT chave, valor FROM mensagens ORDER BY chave").fetchall()

except sqlite3.OperationalError:
print(
    self.prompt_bot + "Ocorreu um problema na gravação da nova integração.")
except sqlite3.IntegrityError:
print(
    self.prompt_bot + "Você informou uma integração já cadastrada.")

except KeyboardInterrupt:
pass


def main():


ChatterBot()


if __name__ == "__main__":
main()
