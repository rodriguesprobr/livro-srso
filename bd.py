#!/usr/bin/python
# -*- coding: utf8 -*-
# Importa a biblioteca pymysql para operacionalizar o Sistema Gerenciador do Banco de Dados
import pymysql

# Cria uma variável global que receberá a conexão com o Sistema Gerenciador do Banco de Dados MySQL
conexao = None


# Função para conectar ao Sistema Gerenciador do Banco de Dados MySQL
def conectar(ip, usuario, senha, base_dados):
    try:
        global conexao
        if conexao is None:
            conexao = pymysql.connect(host=ip,
                                      user=usuario,
                                      password=senha,
                                      database=base_dados,
                                      cursorclass=pymysql.cursors.DictCursor
                                      )
    except pymysql.Error as e:
        print("Erro: {0} - {1} ".format(str(e.args[0]), str(e.args[1])))


# Função para encapsular as consultas ao Sistema Gerenciador do Banco de Dados MySQL
def selecionar(sql):
    cursor = conexao.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


# Função para desconectar ao Sistema Gerenciador do Banco de Dados MySQL
def desconectar():
    conexao.close()
