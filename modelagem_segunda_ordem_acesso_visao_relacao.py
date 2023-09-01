#!/usr/bin/python
# -*- coding: utf8 -*-

from bd import bd
from progress.bar import Bar

deleta_dados = False
insere_dm = False
insere_ap = False
insere_p = False
insere_relacao_grau = True

# Grau de Relação máximo a ser considerado
relacao_grau_max = 3

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
modelagem_direta = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_direta")

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem de Segunda Ordem - Acesso Visão
modelagem_segunda_ordem = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_segunda_ordem_acesso_visao_relacao")

if deleta_dados is True:
    # Exclui dados das dimensões para refrescamento e atualização
    modelagem_segunda_ordem.executar("DELETE FROM acesso;")
    modelagem_segunda_ordem.executar("DELETE FROM servico;")
    modelagem_segunda_ordem.executar("DELETE FROM api;")
    modelagem_segunda_ordem.executar("DELETE FROM api_versao;")
    modelagem_segunda_ordem.executar("DELETE FROM autorizacao_acesso;")
    modelagem_segunda_ordem.executar("DELETE FROM permissao;")
    modelagem_segunda_ordem.executar("DELETE FROM visao;")
    modelagem_segunda_ordem.executar("DELETE FROM relacao_grau;")

# Seleciona dados da Modelagem Direta para formar as dimensões
servicos = modelagem_direta.selecionar("SELECT codigo_servico, nome, url FROM servico WHERE ativo = 1;", None)
apis = modelagem_direta.selecionar("SELECT codigo_api, nome FROM api WHERE ativo = 1;", None)
api_versoes = modelagem_direta.selecionar("SELECT codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url FROM api_versao WHERE ativo = 1;", None)
autorizacoes_acesso = modelagem_direta.selecionar("SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso WHERE ativo = 1;", None)
permissoes = modelagem_direta.selecionar("SELECT codigo_permissao, nome, descricao, url FROM permissao WHERE ativo = 1;", None)
visoes = modelagem_direta.selecionar("SELECT codigo_visao, nome, descricao, url FROM visao WHERE ativo = 1;", None)

if insere_dm is True:
    # Insere dados para a dimensão serviço, a partir da tabela servico da Modelagem Direta, filtrando somente valores ativos
    with Bar("Processando dados da dimensão Serviço", max=len(servicos)) as bar:
        for servico in servicos:
            modelagem_segunda_ordem.inserir(
                "INSERT INTO servico (codigo_servico, nome, url) VALUES (%s, %s, %s);",
                (
                    servico["codigo_servico"],
                    servico["nome"],
                    servico["url"]
                )
            )
            bar.next()

    # Insere dados para a dimensão api, a partir da tabela api da Modelagem Direta, filtrando somente valores ativos
    with Bar("Processando dados da dimensão Application Programming Interface", max=len(apis)) as bar:
        for api in apis:
            modelagem_segunda_ordem.inserir(
                "INSERT INTO api (codigo_api, nome) VALUES (%s, %s);",
                (
                    api["codigo_api"],
                    api["nome"]
                )
            )
            bar.next()

    # Insere dados para a dimensão api_versao, a partir da tabela api_versao da Modelagem Direta, filtrando somente valores ativos
    with Bar("Processando dados da dimensão Versão da Application Programming Interface", max=len(api_versoes)) as bar:
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
            bar.next()

    # Insere dados para a dimensão autorizacao_acesso, a partir da tabela autorizacao_acesso da Modelagem Direta, filtrando somente valores ativos
    with Bar("Processando dados da dimensão Autorização de Acesso", max=len(autorizacoes_acesso)) as bar:
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
            bar.next()

    # Insere dados para a dimensão permissao, a partir da tabela permissao da Modelagem Direta, filtrando somente valores ativos
    with Bar("Processando dados da dimensão Permissão", max=len(permissoes)) as bar:
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
            bar.next()

    # Insere dados para a dimensão visao, a partir da tabela visao da Modelagem Direta, filtrando somente valores ativos
    with Bar("Processando dados da dimensão Visão", max=len(visoes)) as bar:
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
            bar.next()

    # Insere dados para a dimensão relacao_grau, apenas para o grau 1, quando as Visões são acessíveis diretamente
    # por uma Autorização de Acesso ou um cojunto formado por uma Autorização de Acesso e por uma Permissão
    with Bar("Processando dados da dimensão Grau da Relação", max=len(visoes)) as bar:
        for visao in visoes:
            modelagem_segunda_ordem.inserir("INSERT INTO relacao_grau (codigo_relacao_grau, grau) VALUES (1, 1);", None)
            bar.next()

# Seleciona dados da Modelagem de Segunda Ordem para processar a tabela fato
servicos = modelagem_segunda_ordem.selecionar("SELECT codigo_servico, nome, url FROM servico;", None)
apis = modelagem_segunda_ordem.selecionar("SELECT codigo_api, nome FROM api;", None)
api_versoes = modelagem_segunda_ordem.selecionar("SELECT codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url FROM api_versao;", None)
autorizacoes_acesso = modelagem_segunda_ordem.selecionar("SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso;", None)
permissoes = modelagem_segunda_ordem.selecionar("SELECT codigo_permissao, nome, descricao, url FROM permissao;", None)
visoes = modelagem_segunda_ordem.selecionar("SELECT codigo_visao, nome, descricao, url FROM visao;", None)
relacao_graus = modelagem_segunda_ordem.selecionar("SELECT codigo_relacao_grau, grau FROM relacao_grau;", None)


if insere_ap is True:
    with Bar(
            "Processando dados da tabela fato acesso - Acesso às Visões via Autorização de Acesso + Permissão",
            max=(
                    len(servicos) *
                    len(apis) *
                    len(api_versoes) *
                    len(autorizacoes_acesso) *
                    len(permissoes) *
                    len(visoes)
            )
    ) as bar:
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
                                            codigo_relacao_grau,
                                            acesso
                                        ) VALUES (
                                            %s, %s, %s, %s, %s, %s, 1, %s
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
                                bar.next()

if insere_p is True:
    # Insere uma persmissão fantasma, de código 0 para consultas a acesso as Visões sem o uso de Permissões
    modelagem_segunda_ordem.executar("DELETE FROM permissao WHERE codigo_permissao = 0;")
    modelagem_segunda_ordem.inserir("INSERT INTO permissao (codigo_permissao, nome, descricao, url) VALUES (0, 'Sem o uso de Permissão', 'Acesso apenas com o uso de Autorização de Acesso', '');", None)
    with Bar(
            "Processando dados da tabela fato acesso - Acesso às Visões via somente Autorização de Acesso",
            max=(
                    len(servicos) *
                    len(apis) *
                    len(api_versoes) *
                    len(autorizacoes_acesso) *
                    len(visoes)
            )
    ) as bar:
        for servico in servicos:
            for api in apis:
                for api_versao in api_versoes:
                    for autorizacao_acesso in autorizacoes_acesso:
                        for visao in visoes:
                            consulta_acesso = modelagem_direta.selecionar(
                                """
                                    SELECT 
                                        COUNT(*) AS acesso
                                    FROM visao 
                                    INNER JOIN api_versao ON api_versao.codigo_api_versao = visao.codigo_api_versao
                                    INNER JOIN api ON api.codigo_api = visao.codigo_api
                                    INNER JOIN servico ON servico.codigo_servico = api.codigo_servico
                                    INNER JOIN autorizacao_acesso_visao ON autorizacao_acesso_visao.codigo_visao = visao.codigo_visao
                                    WHERE
                                        servico.codigo_servico = %s
                                        AND api.codigo_api = %s
                                        AND api_versao.codigo_api_versao = %s
                                        AND autorizacao_acesso_visao.codigo_autorizacao_acesso = %s
                                        AND visao.codigo_visao = %s
                                """,
                                (
                                    servico["codigo_servico"],
                                    api["codigo_api"],
                                    api_versao["codigo_api_versao"],
                                    autorizacao_acesso["codigo_autorizacao_acesso"],
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
                                        codigo_relacao_grau,
                                        acesso
                                    ) VALUES (
                                        %s, %s, %s, %s, 0, %s, 1, %s
                                    );""",
                                (
                                    servico["codigo_servico"],
                                    api["codigo_api"],
                                    api_versao["codigo_api_versao"],
                                    autorizacao_acesso["codigo_autorizacao_acesso"],
                                    visao["codigo_visao"],
                                    1 if consulta_acesso[0]["acesso"] > 0 else 0
                                )
                            )
                            bar.next()

if insere_relacao_grau is True:
    with Bar("Processando dados para Grau da Relação", max=relacao_grau_max-1) as bar:
        # Iteração para verificar cada grau. TODO: está sem recursividade
        for relacao_grau_verificar in range(2, relacao_grau_max+1):
            # Insere dados para a dimensão relacao_grau, apenas para o grau em questão, quando as Visões são acessíveis
            # por Relação entre Visão de origem (grau anterior) e Visão de destino (grau atual).
            modelagem_segunda_ordem.inserir("INSERT INTO relacao_grau (codigo_relacao_grau, grau) VALUES (%s, %s);", (relacao_grau_verificar, relacao_grau_verificar))

            # Seleciona as Visões do Grau Anterior
            visoes_grau_anterior = modelagem_segunda_ordem.selecionar("""
                SELECT DISTINCT codigo_visao FROM acesso WHERE codigo_relacao_grau = %s""", (relacao_grau_verificar-1)
            )
            with Bar("Processando dados para Grau da Relação - Grau " + str(relacao_grau_verificar), max=len(visoes_grau_anterior)) as bar2:
                for visao_grau_anterior in visoes_grau_anterior:
                    # Seleciona na Modelagem Direta as Visões de destino acessíveis pela Visão
                    visoes_acessiveis = modelagem_direta.selecionar("SELECT DISTINCT codigo_visao_destino FROM relacao WHERE codigo_visao_origem = %s", (visao_grau_anterior["codigo_visao"]))
                    for visao_acessivel in visoes_acessiveis:
                        # Insere os dados da Relação na tabela fato
                        modelagem_segunda_ordem.inserir("""
                            INSERT IGNORE INTO acesso
                                (
                                    codigo_servico,
                                    codigo_api,
                                    codigo_api_versao,
                                    codigo_autorizacao_acesso,
                                    codigo_permissao,
                                    codigo_visao,
                                    codigo_relacao_grau,
                                    acesso
                                )
                            SELECT DISTINCT
                                codigo_servico,
                                codigo_api,
                                codigo_api_versao,
                                codigo_autorizacao_acesso,
                                codigo_permissao,
                                %s,
                                %s,
                                acesso
                            FROM acesso
                            WHERE
                                codigo_visao = %s
                                AND codigo_relacao_grau = %s
                        """, (
                            visao_acessivel["codigo_visao_destino"],
                            relacao_grau_verificar,
                            visao_grau_anterior["codigo_visao"],
                            relacao_grau_verificar-1
                        ))
                    bar2.next()
            bar.next()
