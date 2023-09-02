#!/usr/bin/python
# -*- coding: utf8 -*-

from bd import bd
from progress.bar import Bar

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
modelagem_direta = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_direta")

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem de Segunda Ordem - Acesso Visão
modelagem_segunda_ordem = bd(
    ip="localhost",
    usuario="root",
    senha="",
    base_dados="modelagem_segunda_ordem_acesso_atributo")

# Exclui dados das dimensões para refrescamento e atualização
modelagem_segunda_ordem.executar("DELETE FROM acesso;")
modelagem_segunda_ordem.executar("DELETE FROM autorizacao_acesso;")
modelagem_segunda_ordem.executar("DELETE FROM permissao;")
modelagem_segunda_ordem.executar("DELETE FROM api_versao;")
modelagem_segunda_ordem.executar("DELETE FROM api;")
modelagem_segunda_ordem.executar("DELETE FROM servico;")
modelagem_segunda_ordem.executar("DELETE FROM atributo;")
modelagem_segunda_ordem.executar("DELETE FROM dado_tipo;")
modelagem_segunda_ordem.executar("DELETE FROM visao;")

# Insere dados para a dimensão serviço, a partir da tabela servico da Modelagem Direta, filtrando somente valores ativos
servicos = modelagem_direta.selecionar("SELECT codigo_servico, nome, url FROM servico WHERE ativo = 1;", None)
with Bar("Processando dados da dimensão Serviço", max=len(servicos)) as bar_servico:
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
        apis = modelagem_direta.selecionar("SELECT codigo_api, nome FROM api WHERE ativo = 1 AND codigo_servico = %s;",
                                           (servico["codigo_servico"]))
        with Bar("Processando dados da dimensão Application Programming Interface", max=len(apis)) as bar_api:
            for api in apis:
                modelagem_segunda_ordem.inserir(
                    "INSERT INTO api (codigo_api, codigo_servico, nome) VALUES (%s, %s, %s);",
                    (
                        api["codigo_api"],
                        servico["codigo_servico"],
                        api["nome"]
                    )
                )
                # Insere dados para a dimensão api_versao, a partir da tabela api_versao da Modelagem Direta,
                # filtrando somente valores ativos
                api_versoes = modelagem_direta.selecionar("SELECT codigo_api_versao, numero_versao, data_lancamento, "
                                                          "data_descontinuidade, descricao, url FROM api_versao WHERE "
                                                          "ativo = 1 AND codigo_api = %s;", (api["codigo_api"],))
                with Bar("Processando dados da dimensão Versão da Application Programming Interface",
                         max=len(api_versoes)) as bar_api_versao:
                    for api_versao in api_versoes:
                        modelagem_segunda_ordem.inserir(
                            "INSERT INTO api_versao (codigo_api_versao, codigo_api, numero_versao, data_lancamento, "
                            "data_descontinuidade, descricao, url) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                            (
                                api_versao["codigo_api_versao"],
                                api["codigo_api"],
                                api_versao["numero_versao"],
                                api_versao["data_lancamento"],
                                api_versao["data_descontinuidade"],
                                api_versao["descricao"],
                                api_versao["url"]
                            )
                        )
                        bar_api_versao.next()
                bar_api.next()
        bar_servico.next()

# Insere dados para a dimensão autorizacao_acesso, a partir da tabela autorizacao_acesso da Modelagem Direta,
# filtrando somente valores ativos
autorizacoes_acesso = modelagem_direta.selecionar("SELECT codigo_autorizacao_acesso, nome, descricao, url FROM "
                                                  "autorizacao_acesso WHERE ativo = 1;", None)
with Bar("Processando dados da dimensão Autorização de Acesso", max=len(autorizacoes_acesso)) as bar_autorizacao_acesso:
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
        bar_autorizacao_acesso.next()

# Insere dados para a dimensão permissao, a partir da tabela permissao da Modelagem Direta, filtrando somente valores
# ativos
permissoes = modelagem_direta.selecionar("SELECT codigo_permissao, nome, descricao, url FROM permissao WHERE ativo = 1;"
                                         , None)
with Bar("Processando dados da dimensão Permissão", max=len(permissoes)) as bar_permissao:
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
        bar_permissao.next()

# Insere dados para a dimensão visao, a partir da tabela visao da Modelagem Direta, filtrando somente valores ativos
visoes = modelagem_direta.selecionar("SELECT codigo_visao, nome, descricao, url FROM visao WHERE ativo = 1;", None)
with Bar("Processando dados da dimensão Visão", max=len(visoes)) as bar_visao:
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
        bar_visao.next()

# Insere dados para a dimensão dado_tipo, a partir da tabela dado_tipo da Modelagem Direta, filtrando somente valores
# ativos
dado_tipos = modelagem_direta.selecionar("SELECT codigo_dado_tipo, nome, descricao FROM dado_tipo WHERE ativo = 1;",
                                         None)
with Bar("Processando dados da dimensão Tipo de Dado", max=len(dado_tipos)) as bar_dado_tipo:
    for dado_tipo in dado_tipos:
        modelagem_segunda_ordem.inserir(
            "INSERT INTO dado_tipo (codigo_dado_tipo, nome, descricao) VALUES (%s, %s, %s);",
            (
                dado_tipo["codigo_dado_tipo"],
                dado_tipo["nome"],
                dado_tipo["descricao"]
            )
        )
        bar_dado_tipo.next()

# Insere dados para a dimensão atributo, a partir da tabela atributo da Modelagem Direta, filtrando somente valores
# ativos
atributos = modelagem_direta.selecionar("SELECT codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao "
                                        "FROM atributo WHERE ativo = 1;", None)
with Bar("Processando dados da dimensão Atributos", max=len(atributos)) as bar_atributo:
    for atributo in atributos:
        modelagem_segunda_ordem.inserir(
            "INSERT INTO atributo (codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao) "
            "VALUES (%s, %s, %s, %s, %s);",
            (
                atributo["codigo_atributo"],
                atributo["codigo_visao"],
                atributo["codigo_dado_tipo"],
                atributo["nome"],
                atributo["descricao"]
            )
        )
        bar_atributo.next()

with Bar(
        "Processando dados da tabela fato acesso - Acesso aos Atributos via Autorização de Acesso + Permissão",
        max=(
                len(api_versoes) *
                len(autorizacoes_acesso) *
                len(permissoes) *
                len(atributos)
        )
) as bar_acesso:
    api_versoes = modelagem_segunda_ordem.selecionar("SELECT codigo_api_versao, numero_versao, data_lancamento, "
                                              "data_descontinuidade, descricao, url FROM api_versao;", None)
    for api_versao in api_versoes:
        autorizacoes_acesso = modelagem_segunda_ordem.selecionar("SELECT codigo_autorizacao_acesso, nome, descricao, "
                                                                 "url FROM autorizacao_acesso;", None)
        for autorizacao_acesso in autorizacoes_acesso:
            permissoes = modelagem_segunda_ordem.selecionar("SELECT codigo_permissao, nome, descricao, url FROM "
                                                            "permissao;", None)
            for permissao in permissoes:
                atributos = modelagem_segunda_ordem.selecionar("SELECT codigo_atributo, codigo_visao, codigo_dado_tipo,"
                                                               " nome, descricao FROM atributo;", None)
                for atributo in atributos:
                        consulta_acesso = modelagem_direta.selecionar(
                            """
                                SELECT 
                                    COUNT(*) AS acesso
                                FROM atributo 
                                INNER JOIN visao ON visao.codigo_visao = atributo.codigo_visao
                                INNER JOIN api_versao ON api_versao.codigo_api_versao = visao.codigo_api_versao
                                INNER JOIN autorizacao_acesso_permissao_atributo ON autorizacao_acesso_permissao_atributo.codigo_atributo = atributo.codigo_atributo
                                WHERE
                                    api_versao.codigo_api_versao = %s
                                    AND autorizacao_acesso_permissao_atributo.codigo_autorizacao_acesso = %s
                                    AND autorizacao_acesso_permissao_atributo.codigo_permissao = %s
                                    AND atributo.codigo_atributo = %s
                            """,
                            (
                                api_versao["codigo_api_versao"],
                                autorizacao_acesso["codigo_autorizacao_acesso"],
                                permissao["codigo_permissao"],
                                atributo["codigo_atributo"]
                            )
                        )
                        modelagem_segunda_ordem.inserir(
                            """INSERT INTO acesso 
                                (
                                    codigo_api_versao,
                                    codigo_autorizacao_acesso,
                                    codigo_permissao,
                                    codigo_atributo,
                                    acesso
                                ) VALUES (
                                    %s, %s, %s, %s, %s
                                );""",
                            (
                                api_versao["codigo_api_versao"],
                                autorizacao_acesso["codigo_autorizacao_acesso"],
                                permissao["codigo_permissao"],
                                atributo["codigo_atributo"],
                                1 if consulta_acesso[0]["acesso"] > 0 else 0
                            )
                        )
                        bar_acesso.next()

# Insere uma persmissão fantasma, de código 0 para consultar a acesso aos Atributos sem o uso de Permissões
modelagem_segunda_ordem.executar("DELETE FROM permissao WHERE codigo_permissao = 0;")
modelagem_segunda_ordem.inserir("INSERT INTO permissao (codigo_permissao, nome, descricao, url) VALUES (0, "
                                "'Sem o uso de Permissão', 'Acesso apenas com o uso de Autorização de Acesso', '');",
                                None)
with Bar(
        "Processando dados da tabela fato acesso - Acesso aos Atributos via Autorização de Acesso + Permissão",
        max=(
                len(api_versoes) *
                len(autorizacoes_acesso) *
                len(atributos)
        )
) as bar_acesso:
    api_versoes = modelagem_segunda_ordem.selecionar("SELECT codigo_api_versao, numero_versao, data_lancamento, "
                                                     "data_descontinuidade, descricao, url FROM api_versao;", None)
    for api_versao in api_versoes:
        autorizacoes_acesso = modelagem_segunda_ordem.selecionar("SELECT codigo_autorizacao_acesso, nome, descricao, "
                                                                 "url FROM autorizacao_acesso;", None)
        for autorizacao_acesso in autorizacoes_acesso:
            for atributo in atributos:
                atributos = modelagem_segunda_ordem.selecionar("SELECT codigo_atributo, codigo_visao, codigo_dado_tipo,"
                                                               " nome, descricao FROM atributo;", None)
                consulta_acesso = modelagem_direta.selecionar(
                    """
                        SELECT 
                            COUNT(*) AS acesso
                        FROM atributo 
                        INNER JOIN visao ON visao.codigo_visao = atributo.codigo_visao
                        INNER JOIN api_versao ON api_versao.codigo_api_versao = visao.codigo_api_versao
                        INNER JOIN autorizacao_acesso_atributo aaa 
                            ON autorizacao_acesso_atributo.codigo_atributo = atributo.codigo_atributo
                        WHERE
                            api_versao.codigo_api_versao = %s
                            AND autorizacao_acesso_atributo.codigo_autorizacao_acesso = %s
                            AND atributo.codigo_atributo = %s
                    """,
                    (
                        api_versao["codigo_api_versao"],
                        autorizacao_acesso["codigo_autorizacao_acesso"],
                        atributo["codigo_atributo"]
                    )
                )
                modelagem_segunda_ordem.inserir(
                    """INSERT INTO acesso 
                        (
                            codigo_api_versao,
                            codigo_autorizacao_acesso,
                            codigo_permissao,
                            codigo_atributo,
                            acesso
                        ) VALUES (
                            %s, %s, 0, %s, %s
                        );""",
                    (
                        api_versao["codigo_api_versao"],
                        autorizacao_acesso["codigo_autorizacao_acesso"],
                        atributo["codigo_atributo"],
                        1 if consulta_acesso[0]["acesso"] > 0 else 0
                    )
                )
                bar_acesso.next()
