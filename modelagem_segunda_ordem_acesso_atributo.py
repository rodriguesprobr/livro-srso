#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Este script gera o terceiro DataMart do livro.

Utiliza a classe bd do arquivo bd.py para realizar a conexão com o Sistema Gerenciador do Banco de Dados MySQL/MariaDB.
"""

from progress.bar import Bar  # Importa a biblioteca progress para exibir uma barra de progresso
from bd import bd  # Importa a classe bd do arquivo bd.py

__author__ = "Fernando de Assis Rodrigues"
__copyright__ = "2023 - Fernando de Assis Rodrigues"
__credits__ = ["Fernando de Assis Rodrigues"]
__license__ = "Creative Commons 4.0 BY-SA-ND"
__version__ = "1.0"
__maintainer__ = "Fernando de Assis Rodrigues"
__email__ = "fernando@rodrigues.pro.br"
__status__ = "Produção"

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
# Personalizar as informações ip, usuario, senha e base_dados de acordo com a instalação do MySQL/MariaDB
modelagem_direta = bd(ip="localhost", usuario="usuario_do_banco_de_dados", senha="senha", base_dados="modelagem_direta")

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem de Segunda Ordem - Acesso Atributo
# Personalizar as informações ip, usuario, senha e base_dados de acordo com a instalação do MySQL/MariaDB
modelagem_segunda_ordem = bd(
    ip="localhost",
    usuario="usuario_do_banco_de_dados",
    senha="senha",
    base_dados="modelagem_segunda_ordem_acesso_atributo")

# Exclui dados das dimensões para refrescamento e atualização
modelagem_segunda_ordem.executar("DELETE FROM acesso WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM autorizacao_acesso WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM permissao WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM api_versao WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM api WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM servico WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM atributo WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM dado_tipo WHERE 1;")
modelagem_segunda_ordem.executar("DELETE FROM visao WHERE 1;")

# Insere dados para a dimensão serviço, a partir da tabela servico da Modelagem Direta, filtrando somente valores ativos
servicos = modelagem_direta.selecionar("SELECT codigo_servico, nome, url FROM servico WHERE ativo = %s;", 1)
with Bar("Processando dados da dimensão Serviço", max=len(servicos)) as bar_servico:
    for servico in servicos:
        modelagem_segunda_ordem.inserir(
            "INSERT INTO servico (codigo_servico, nome, url) VALUES (%s, %s, %s);",
            (servico["codigo_servico"], servico["nome"], servico["url"])
        )
        # Insere dados para a dimensão api, a partir da tabela api da Modelagem Direta, filtrando somente valores ativos
        apis = modelagem_direta.selecionar(
            "SELECT codigo_api, nome FROM api WHERE ativo = %s AND codigo_servico = %s;",
            (1, servico["codigo_servico"]))
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
                api_versoes = modelagem_direta.selecionar(
                    """
                    SELECT
                        codigo_api_versao,
                        numero_versao,
                        data_lancamento,
                        data_descontinuidade,
                        descricao,
                        url
                    FROM api_versao
                    WHERE 
                        ativo = %s
                        AND codigo_api = %s;""",
                    (1, api["codigo_api"],))
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
autorizacoes_acesso = modelagem_direta.selecionar(
    """SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso WHERE ativo = %s;""",
    1)
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
permissoes = modelagem_direta.selecionar(
    "SELECT codigo_permissao, nome, descricao, url FROM permissao WHERE ativo = %s;",
    1)
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
visoes = modelagem_direta.selecionar(
    "SELECT codigo_visao, nome, descricao, url FROM visao WHERE ativo = %s;",
    1)
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
dado_tipos = modelagem_direta.selecionar(
    "SELECT codigo_dado_tipo, nome, descricao FROM dado_tipo WHERE ativo = %s;",
    1)
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
atributos = modelagem_direta.selecionar(
    "SELECT codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao FROM atributo WHERE ativo = %s;",
    1)
with Bar("Processando dados da dimensão Atributos", max=len(atributos)) as bar_atributo:
    for atributo in atributos:
        modelagem_segunda_ordem.inserir(
            """
                INSERT INTO
                    atributo
                        (codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao)
                VALUES (%s, %s, %s, %s, %s);""",
            (
                atributo["codigo_atributo"],
                atributo["codigo_visao"],
                atributo["codigo_dado_tipo"],
                atributo["nome"],
                atributo["descricao"]
            )
        )
        bar_atributo.next()

api_versoes = modelagem_segunda_ordem.selecionar("""
    SELECT
        codigo_api_versao,
        numero_versao,
        data_lancamento,
        data_descontinuidade,
        descricao,
        url 
    FROM api_versao;""", None)
with Bar(
        "Processando dados da tabela fato acesso - Acesso aos Atributos via Autorização de Acesso + Permissão",
        max=(
                len(api_versoes) *
                len(autorizacoes_acesso) *
                len(permissoes) *
                len(atributos)
        )
) as bar_acesso:
    for api_versao in api_versoes:
        autorizacoes_acesso = modelagem_segunda_ordem.selecionar(
            "SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso;", None)
        for autorizacao_acesso in autorizacoes_acesso:
            permissoes = modelagem_segunda_ordem.selecionar(
                "SELECT codigo_permissao, nome, descricao, url FROM permissao;", None)
            for permissao in permissoes:
                atributos = modelagem_segunda_ordem.selecionar(
                    "SELECT codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao FROM atributo;",
                    None)
                sql = """INSERT INTO acesso 
                            (
                                codigo_api_versao,
                                codigo_autorizacao_acesso,
                                codigo_permissao,
                                codigo_atributo,
                                acesso
                            ) VALUES"""
                for atributo in atributos:
                    consulta_acesso = modelagem_direta.selecionar(
                        """
                            SELECT 
                                COUNT(*) AS acesso
                            FROM atributo a
                            INNER JOIN visao v ON v.codigo_visao = a.codigo_visao
                            INNER JOIN api_versao av ON av.codigo_api_versao = v.codigo_api_versao
                            INNER JOIN autorizacao_acesso_permissao_atributo aapa 
                                ON aapa.codigo_atributo = a.codigo_atributo
                            WHERE
                                av.codigo_api_versao = %s
                                AND aapa.codigo_autorizacao_acesso = %s
                                AND aapa.codigo_permissao = %s
                                AND a.codigo_atributo = %s
                        """,
                        (
                            api_versao["codigo_api_versao"],
                            autorizacao_acesso["codigo_autorizacao_acesso"],
                            permissao["codigo_permissao"],
                            atributo["codigo_atributo"]
                        )
                    )
                    sql += "(%s, %s, %s, %s, %s)," % (
                        api_versao["codigo_api_versao"],
                        autorizacao_acesso["codigo_autorizacao_acesso"],
                        permissao["codigo_permissao"],
                        atributo["codigo_atributo"],
                        1 if consulta_acesso[0]["acesso"] > 0 else 0
                    )
                    bar_acesso.next()
                modelagem_segunda_ordem.inserir(sql.rstrip(sql[-1]), None)

# Insere uma permissão fantasma, de código 0 para consultar a acesso aos Atributos sem o uso de Permissões
modelagem_segunda_ordem.executar("DELETE FROM permissao WHERE codigo_permissao = 0;")
modelagem_segunda_ordem.inserir(
    """
        INSERT INTO
            permissao (codigo_permissao, nome, descricao, url) 
        VALUES (0, 'Sem o uso de Permissão', 'Acesso apenas com o uso de Autorização de Acesso', '');""",
    None)
api_versoes = modelagem_segunda_ordem.selecionar(
    """
        SELECT 
            codigo_api_versao,
            numero_versao,
            data_lancamento,
            data_descontinuidade,
            descricao,
            url 
        FROM api_versao;""",
    None)
with Bar(
        "Processando dados da tabela fato acesso - Acesso aos Atributos via Autorização de Acesso",
        max=(
                len(api_versoes) *
                len(autorizacoes_acesso) *
                len(atributos)
        )
) as bar_acesso:
    for api_versao in api_versoes:
        autorizacoes_acesso = modelagem_segunda_ordem.selecionar(
            "SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso;",
            None)
        for autorizacao_acesso in autorizacoes_acesso:
            sql = """INSERT INTO acesso 
                        (
                            codigo_api_versao,
                            codigo_autorizacao_acesso,
                            codigo_permissao,
                            codigo_atributo,
                            acesso
                        ) VALUES"""
            for atributo in atributos:
                atributos = modelagem_segunda_ordem.selecionar(
                    "SELECT codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao FROM atributo;",
                    None)
                consulta_acesso = modelagem_direta.selecionar(
                    """
                        SELECT 
                            COUNT(*) AS acesso
                        FROM atributo a
                        INNER JOIN visao v ON v.codigo_visao = a.codigo_visao
                        INNER JOIN api_versao av ON av.codigo_api_versao = v.codigo_api_versao
                        INNER JOIN autorizacao_acesso_atributo aaa 
                            ON aaa.codigo_atributo = a.codigo_atributo
                        WHERE
                            av.codigo_api_versao = %s
                            AND aaa.codigo_autorizacao_acesso = %s
                            AND a.codigo_atributo = %s
                    """,
                    (
                        api_versao["codigo_api_versao"],
                        autorizacao_acesso["codigo_autorizacao_acesso"],
                        atributo["codigo_atributo"]
                    )
                )
                sql += "(%s, %s, %s, %s, %s)," % (
                    api_versao["codigo_api_versao"],
                    autorizacao_acesso["codigo_autorizacao_acesso"],
                    0,
                    atributo["codigo_atributo"],
                    1 if consulta_acesso[0]["acesso"] > 0 else 0
                )
                bar_acesso.next()
            modelagem_segunda_ordem.inserir(sql.rstrip(sql[-1]), None)
