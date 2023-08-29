#!/usr/bin/python
# -*- coding: utf8 -*-

from bd import bd

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
modelagem_direta = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_direta")

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem de Segunda Ordem - Acesso Visão
modelagem_segunda_ordem = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_segunda_ordem_acesso_visao")

# Exclui dados das dimensões para refrescamento e atualização
modelagem_segunda_ordem.executar("DELETE FROM servico;")
modelagem_segunda_ordem.executar("DELETE FROM api;")
modelagem_segunda_ordem.executar("DELETE FROM api_versao;")
modelagem_segunda_ordem.executar("DELETE FROM autorizacao_acesso;")
modelagem_segunda_ordem.executar("DELETE FROM permissao;")
modelagem_segunda_ordem.executar("DELETE FROM visao;")
modelagem_segunda_ordem.executar("DELETE FROM acesso;")

# Seleciona dados da Modelagem Direta para formar as dimensões
servicos = modelagem_direta.selecionar("SELECT codigo_servico, nome, url FROM servico WHERE ativo = 1;", None)
apis = modelagem_direta.selecionar("SELECT codigo_api, nome FROM api WHERE ativo = 1;", None)
api_versoes = modelagem_direta.selecionar("SELECT codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url FROM api_versao WHERE ativo = 1;", None)
autorizacoes_acesso = modelagem_direta.selecionar("SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso WHERE ativo = 1;", None)
permissoes = modelagem_direta.selecionar("SELECT codigo_permissao, nome, descricao, url FROM permissao WHERE ativo = 1;", None)
visoes = modelagem_direta.selecionar("SELECT codigo_visao, nome, descricao, url FROM visao WHERE ativo = 1;", None)

# Insere dados para a dimensão serviço, a partir da tabela servico da Modelagem Direta, filtrando somente valores ativos
for servico in servicos:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO servico (codigo_servico, nome, url) VALUES (%s, %s, %s);",
        (
            servico["codigo_servico"],
            servico["nome"],
            servico["url"]
        )
    )

# Insere dados para a dimensão api, a partir da tabela api da Modelagem Direta, filtrando somente valores ativos
for api in apis:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO api (codigo_api, nome) VALUES (%s, %s);",
        (
            api["codigo_api"],
            api["nome"]
        )
    )

# Insere dados para a dimensão api_versao, a partir da tabela api_versao da Modelagem Direta, filtrando somente valores ativos
for api_versao in api_versoes:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO api_versao (codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url) VALUES (%s, %s, %s, %s, %s, %s);",
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
        "INSERT INTO autorizacao_acesso (codigo_autorizacao_acesso, nome, descricao, url) VALUES (%s, %s, %s, %s);",
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
        "INSERT INTO permissao (codigo_permissao, nome, descricao, url) VALUES (%s, %s, %s, %s);",
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
        "INSERT INTO visao (codigo_visao, nome, descricao, url) VALUES (%s, %s, %s, %s);",
        (
            visao["codigo_visao"],
            visao["nome"],
            visao["descricao"],
            visao["url"]
        )
    )

for servico in servicos:
    for api in apis:
        for api_versao in api_versoes:
            for autorizacao_acesso in autorizacoes_acesso:
                for permissao in permissoes:
                    for visao in visoes:
                        consulta_acesso = modelagem_direta.selecionar(
                            """
                                SELECT 
                                    COUNT(*) AS acesso
                                FROM visao 
                                INNER JOIN api_versao ON api_versao.codigo_api_versao = visao.codigo_api_versao
                                INNER JOIN api ON api.codigo_api = visao.codigo_api
                                INNER JOIN servico ON servico.codigo_servico = api.codigo_servico
                                INNER JOIN autorizacao_acesso_permissao_visao ON autorizacao_acesso_permissao_visao.codigo_visao = visao.codigo_visao
                                WHERE
                                    servico.codigo_servico = %s
                                    AND api.codigo_api = %s
                                    AND api_versao.codigo_api_versao = %s
                                    AND autorizacao_acesso_permissao_visao.codigo_autorizacao_acesso = %s
                                    AND autorizacao_acesso_permissao_visao.codigo_permissao = %s
                                    AND visao.codigo_visao = %s
                            """,
                            (
                                servico["codigo_servico"],
                                api["codigo_api"],
                                api_versao["codigo_api_versao"],
                                autorizacao_acesso["codigo_autorizacao_acesso"],
                                permissao["codigo_permissao"],
                                visao["codigo_visao"]
                            )
                        )
                        modelagem_segunda_ordem.inserir(
                            """INSERT INTO acesso 
                                (
                                    codigo_servico,
                                    codigo_api,
                                    codigo_api_versao,
                                    codigo_autorizacao_acesso,
                                    codigo_permissao,
                                    codigo_visao,
                                    acesso
                                ) VALUES (
                                    %s, %s, %s, %s, %s, %s, %s
                                );""",
                            (
                                servico["codigo_servico"],
                                api["codigo_api"],
                                api_versao["codigo_api_versao"],
                                autorizacao_acesso["codigo_autorizacao_acesso"],
                                permissao["codigo_permissao"],
                                visao["codigo_visao"],
                                1 if consulta_acesso[0]["acesso"] > 0 else 0
                            )
                        )