#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Classe bd para realizar a conexão com o Sistema Gerenciador do Banco de Dados MySQL/MariaDB.

Este script em python é invocado pelos outros scripts do projeto, para evitar que seja necessário a repetição de
funções de conexão, desconexão, seleção, execução e inserção de dados.
"""

import pymysql  # Importa a biblioteca pymysql para operacionalizar o Sistema Gerenciador do Banco de Dados
import sys  # Importa a biblioteca sys para controle do sistema

__author__ = "Fernando de Assis Rodrigues"
__copyright__ = "2023 - Fernando de Assis Rodrigues"
__credits__ = ["Fernando de Assis Rodrigues"]
__license__ = "Creative Commons 4.0 BY-NC-SA"
__version__ = "1.0"
__maintainer__ = "Fernando de Assis Rodrigues"
__email__ = "fernando@rodrigues.pro.br"
__status__ = "Produção"


# Cria uma classe bd de conexão.
class bd:

    def __init__(self, ip, usuario, senha, base_dados):
        # Cria uma variável que receberá a conexão com o Sistema Gerenciador do Banco de Dados MySQL/MariaDB
        self.conexao = None
        # Cria uma variável que receberá o cursor das consultas
        self.cursor = None
        # Conecta no Sistema Gerenciador do Banco de Dados MySQL/MariaDB
        self.conectar(ip, usuario, senha, base_dados)

    # Função para conectar ao Sistema Gerenciador do Banco de Dados MySQL/MariaDB
    def conectar(self, ip, usuario, senha, base_dados):
        try:
            while self.conexao is None:
                self.conexao = pymysql.connect(host=ip,
                                               user=usuario,
                                               password=senha,
                                               database=base_dados,
                                               cursorclass=pymysql.cursors.DictCursor
                                               )
        except pymysql.Error as e:
            print("Erro: {0} - {1} ".format(str(e.args[0]), str(e.args[1])))
            sys.exit(1)

    # Função para encapsular as consultas ao Sistema Gerenciador do Banco de Dados MySQL/MariaDB
    def selecionar(self, sql, valores):
        self.cursor = self.conexao.cursor()
        self.cursor.execute(sql, valores)
        return self.cursor.fetchall()

    def executar(self, sql):
        self.cursor = self.conexao.cursor()
        estado = None
        try:
            estado = self.cursor.execute(sql)
        except pymysql.Error as err:
            print("Erro: {0} - {1} ".format(str(err.args[0]), str(err.args[1])))
            sys.exit(1)
        if estado is not None:
            self.conexao.commit()
        return estado

    def inserir(self, sql, valores):
        self.cursor = self.conexao.cursor()
        estado = None
        try:
            estado = self.cursor.execute(sql, valores)
        except pymysql.Error as err:
            print("Erro: {0} - {1} ".format(str(err.args[0]), str(err.args[1])))
            sys.exit(1)
        if estado is not None:
            self.conexao.commit()
        return estado

    # Função para desconectar ao Sistema Gerenciador do Banco de Dados MySQL/MariaDB
    def desconectar(self):
        self.conexao.close()
