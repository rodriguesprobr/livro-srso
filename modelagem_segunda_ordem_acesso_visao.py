#!/usr/bin/python
# -*- coding: utf8 -*-

from bd import bd

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
modelagem_direta = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_segunda_ordem_acesso_visao")

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem de Segunda Ordem - Acesso Visão
modelagem_segunda_ordem = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_segunda_ordem_acesso_visao")

# Exclui dados das dimensões para refrescamento e atualização
modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.servico;")
modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.api;")
modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.api_versao;")
modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.autorizacao_acesso;")
modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.permissao;")
modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.visao;")

# Seleciona dados da Modelagem Direta para formar as dimensões
servicos = modelagem_direta.selecionar("SELECT codigo_servico, nome, url FROM modelagem_direta.servico WHERE ativo = 1;")
apis = modelagem_direta.selecionar("SELECT codigo_api, nome FROM modelagem_direta.api WHERE ativo = 1;")
api_versoes = modelagem_direta.selecionar("SELECT codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url FROM modelagem_direta.api_versao WHERE ativo = 1;")
autorizacoes_acesso = modelagem_direta.selecionar("SELECT codigo_autorizacao_acesso, nome, descricao, url FROM modelagem_direta.autorizacao_acesso WHERE ativo = 1;")
permissoes = modelagem_direta.selecionar("SELECT codigo_permissao, nome, descricao, url FROM modelagem_direta.permissao WHERE ativo = 1;")
visoes = modelagem_direta.selecionar("SELECT codigo_visao, nome, descricao, url FROM modelagem_direta.visao WHERE ativo = 1;")

# Insere dados para a dimensão serviço, a partir da tabela servico da Modelagem Direta, filtrando somente valores ativos
for servico in servicos:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO modelagem_segunda_ordem_acesso_visao.servico (codigo_servico, nome, url) VALUES (%s, %s, %s);",
        (
            servico["codigo_servico"],
            servico["nome"],
            servico["url"]
        )
    )

# Insere dados para a dimensão api, a partir da tabela api da Modelagem Direta, filtrando somente valores ativos
for api in apis:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO modelagem_segunda_ordem_acesso_visao.api (codigo_api, nome) VALUES (%s, %s);",
        (
            api["codigo_api"],
            api["nome"]
        )
    )

# Insere dados para a dimensão api_versao, a partir da tabela api_versao da Modelagem Direta, filtrando somente valores ativos
for api_versao in api_versoes:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO modelagem_segunda_ordem_acesso_visao.api_versao (codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url) VALUES (%s, %s, %s, %s, %s, %s);",
        (
            api_versao["codigo_api_versao"],
            api_versao["numero_versao"],
            api_versao["data_lancamento"],
            api_versao["data_descontinuidade"],
            api_versao["descricao"],
            api_versao["url"]
        )
    )

# Insere dados para a dimensão autorizacao_acesso, a partir da tabela autorizacao_acesso da Modelagem Direta, filtrando somente valores ativos
for autorizacao_acesso in autorizacoes_acesso:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO modelagem_segunda_ordem_acesso_visao.autorizacao_acesso (codigo_autorizacao_acesso, nome, descricao, url) VALUES (%s, %s, %s, %s);",
        (
            autorizacao_acesso["codigo_autorizacao_acesso"],
            autorizacao_acesso["nome"],
            autorizacao_acesso["descricao"],
            autorizacao_acesso["url"]
        )
    )

# Insere dados para a dimensão permissao, a partir da tabela permissao da Modelagem Direta, filtrando somente valores ativos
for permissao in permissoes:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO modelagem_segunda_ordem_acesso_visao.permissao (codigo_permissao, nome, descricao, url) VALUES (%s, %s, %s, %s);",
        (
            permissao["codigo_permissao"],
            permissao["nome"],
            permissao["descricao"],
            permissao["url"]
        )
    )

# Insere dados para a dimensão visao, a partir da tabela permissao da Modelagem Direta, filtrando somente valores ativos
for visao in visoes:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO modelagem_segunda_ordem_acesso_visao.visao (codigo_visao, nome, descricao, url) VALUES (%s, %s, %s, %s);",
        (
            visao["codigo_visao"],
            visao["nome"],
            visao["descricao"],
            visao["url"]
        )
    )