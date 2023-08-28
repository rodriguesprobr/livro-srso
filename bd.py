#!/usr/bin/python
# -*- coding: utf8 -*-
# Importa a biblioteca pymysql para operacionalizar o Sistema Gerenciador do Banco de Dados
import pymysql


# Cria uma classe bd de conexão.
class bd:

    def __init__(self, ip, usuario, senha, base_dados):
        # Cria uma variável global que receberá a conexão com o Sistema Gerenciador do Banco de Dados MySQL
        self.conexao = None

        # Conecta no Sistema Gerenciador do Banco de Dados MySQL
        self.conectar(
            ip,
            usuario,
            senha,
            base_dados
        )

    # Função para conectar ao Sistema Gerenciador do Banco de Dados MySQL
    def conectar(self, ip, usuario, senha, base_dados):
        try:
            if self.conexao is None:
                self.conexao = pymysql.connect(host=ip,
                                          user=usuario,
                                          password=senha,
                                          database=base_dados,
                                          cursorclass=pymysql.cursors.DictCursor
                                          )
        except pymysql.Error as e:
            print("Erro: {0} - {1} ".format(str(e.args[0]), str(e.args[1])))

    # Função para encapsular as consultas ao Sistema Gerenciador do Banco de Dados MySQL
    def selecionar(self, sql):
        self.cursor = self.conexao.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def executar(self, sql):
        self.cursor = self.conexao.cursor()
        estado = None
        try:
            estado = self.cursor.execute(sql)
        except pymysql.Error as err:
            print("Erro: " + str(err))
        if estado != None:
            self.conexao.commit()
        return estado

    def inserir(self, sql, valores):
        self.cursor = self.conexao.cursor()
        estado = None
        try:
            estado = self.cursor.execute(sql, valores)
        except pymysql.Error as err:
            print("Erro: " + str(err))
        if estado != None:
            self.conexao.commit()
        return estado

    # Função para desconectar ao Sistema Gerenciador do Banco de Dados MySQL
    def desconectar(self):
        self.conexao.close()
