#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Este script gera o quarto DataMart do livro.

Utiliza a classe bd do arquivo bd.py para realizar a conexão com o Sistema Gerenciador do Banco de Dados MySQL/MariaDB.
"""

from progress.bar import Bar  # Importa a biblioteca progress para exibir uma barra de progresso
from bd import bd  # Importa a classe bd do arquivo bd.py

__author__ = "Fernando de Assis Rodrigues"
__copyright__ = "2023 - Fernando de Assis Rodrigues"
__credits__ = ["Fernando de Assis Rodrigues"]
__license__ = "Creative Commons 4.0 BY-NC-SA"
__version__ = "1.0"
__maintainer__ = "Fernando de Assis Rodrigues"
__email__ = "fernando@rodrigues.pro.br"
__status__ = "Produção"

# Grau de Relação máximo a ser considerado
relacao_grau_max = 2

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
# Personalizar as informações ip, usuario, senha e base_dados de acordo com a instalação do MySQL/MariaDB
modelagem_direta = bd(ip="localhost", usuario="usuario_do_banco_de_dados", senha="senha", base_dados="modelagem_direta")

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem de Segunda Ordem - Acesso Atributo/Relação
# Personalizar as informações ip, usuario, senha e base_dados de acordo com a instalação do MySQL/MariaDB
modelagem_segunda_ordem = bd(
    ip="localhost",
    usuario="usuario_do_banco_de_dados",
    senha="senha",
    base_dados="modelagem_segunda_ordem_acesso_atributo_relacao")

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
modelagem_segunda_ordem.executar("DELETE FROM relacao_grau WHERE 1;")

# Insere dados para a dimensão serviço, a partir da tabela servico da Modelagem Direta, filtrando somente valores ativos
servicos = modelagem_direta.selecionar(
    "SELECT codigo_servico, nome, url FROM servico WHERE ativo = %s;",
    1)
with Bar("Processando dados da dimensão Serviço",
         max=len(servicos)) as bar_servico:
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
                            """
                                INSERT INTO
                                    api_versao 
                                    (
                                        codigo_api_versao,
                                        codigo_api,
                                        numero_versao,
                                        data_lancamento,
                                        data_descontinuidade,
                                        descricao,
                                        url
                                    ) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s);""",
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
    "SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso WHERE ativo = %s;",
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
with Bar("Processando dados da dimensão Permissão",
         max=len(permissoes)) as bar_permissao:
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
                        (
                            codigo_atributo, 
                            codigo_visao, 
                            codigo_dado_tipo, 
                            nome, 
                            descricao
                        ) 
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

# Insere dados para a dimensão relacao_grau, apenas para o grau 1, quando os Atributos são acessíveis diretamente
# por uma Autorização de Acesso ou um conjunto formado por uma Autorização de Acesso e por uma Permissão
with Bar("Processando dados da dimensão Grau da Relação", max=1) as bar_relacao_grau:
    modelagem_segunda_ordem.inserir(
        "INSERT INTO relacao_grau (codigo_relacao_grau, grau) VALUES (%s, %s);",
        (1, 1))
    bar_relacao_grau.next()

api_versoes = modelagem_segunda_ordem.selecionar(
    "SELECT codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url FROM api_versao;",
    None)
for api_versao_indice, api_versao in enumerate(api_versoes):
    autorizacoes_acesso = modelagem_segunda_ordem.selecionar(
        "SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso;",
        None)
    for autorizacao_acesso_indice, autorizacao_acesso in enumerate(autorizacoes_acesso):
        permissoes = modelagem_segunda_ordem.selecionar(
            "SELECT codigo_permissao, nome, descricao, url FROM permissao;",
            None)
        for permissao_indice, permissao in enumerate(permissoes):
            print(
                    "Versão de API (%s/%s) - Autorização de Acesso (%s/%s) - Permissão (%s/%s)"
                    % (
                        api_versao_indice+1,
                        len(api_versoes),
                        autorizacao_acesso_indice+1,
                        len(autorizacoes_acesso),
                        permissao_indice+1,
                        len(permissoes)
                    )
            )
            atributos = modelagem_segunda_ordem.selecionar(
                "SELECT codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao FROM atributo;",
                None)

            sql = """
                INSERT INTO 
                    acesso
                        (
                            codigo_api_versao,
                            codigo_autorizacao_acesso,
                            codigo_permissao,
                            codigo_atributo, 
                            codigo_relacao_grau,
                            acesso
                        ) 
                    VALUES 
            """
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
                sql += "(%s, %s, %s, %s, %s, %s)," % (
                    api_versao["codigo_api_versao"],
                    autorizacao_acesso["codigo_autorizacao_acesso"],
                    permissao["codigo_permissao"],
                    atributo["codigo_atributo"],
                    1,
                    1 if consulta_acesso[0]["acesso"] > 0 else 0
                )
            modelagem_segunda_ordem.inserir(sql.rstrip(sql[-1]), None)

# Insere uma permissão fantasma, de código 0 para consultar a acesso aos Atributos sem o uso de Permissões
modelagem_segunda_ordem.executar("DELETE FROM permissao WHERE codigo_permissao = 0;")
modelagem_segunda_ordem.inserir(
    """
        INSERT INTO
            permissao (
                codigo_permissao, 
                nome, 
                descricao, 
                url
            ) VALUES (%s, %s, %s, %s)
    """,
    (
        0,
        "Sem o uso de Permissão",
        "Acesso apenas com o uso de Autorização de Acesso",
        ""
    )
)
api_versoes = modelagem_segunda_ordem.selecionar(
    "SELECT codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url FROM api_versao;",
    None)
for api_versao_indice, api_versao in enumerate(api_versoes):
    autorizacoes_acesso = modelagem_segunda_ordem.selecionar(
        "SELECT codigo_autorizacao_acesso, nome, descricao, url FROM autorizacao_acesso;",
        None)
    for autorizacao_acesso_indice, autorizacao_acesso in enumerate(autorizacoes_acesso):
        print(
            "Versão de API (%s/%s) - Autorização de Acesso (%s/%s)"
            % (
                api_versao_indice + 1,
                len(api_versoes),
                autorizacao_acesso_indice + 1,
                len(autorizacoes_acesso)
            )
        )
        atributos = modelagem_segunda_ordem.selecionar(
            "SELECT codigo_atributo, codigo_visao, codigo_dado_tipo, nome, descricao FROM atributo;",
            None)

        sql = """
            INSERT INTO 
                acesso 
                    (
                        codigo_api_versao,
                        codigo_autorizacao_acesso, 
                        codigo_permissao, 
                        codigo_atributo, 
                        codigo_relacao_grau, 
                        acesso
                    ) VALUES
        """
        for atributo in atributos:
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
            sql += "(%s, %s, %s, %s, %s, %s)," % (
                api_versao["codigo_api_versao"],
                autorizacao_acesso["codigo_autorizacao_acesso"],
                0,
                atributo["codigo_atributo"],
                1,
                1 if consulta_acesso[0]["acesso"] > 0 else 0
            )
        modelagem_segunda_ordem.inserir(sql.rstrip(sql[-1]), None)


with Bar("Processando dados para Grau da Relação", max=relacao_grau_max - 1) as bar_relacoes_grau:
    # Iteração para verificar cada grau. TODO: está sem recursividade
    for relacao_grau_verificar in range(2, relacao_grau_max + 1):
        # Insere dados para a dimensão relacao_grau, apenas para o grau em questão, quando as Visões são acessíveis
        # por Relação entre Visão de origem (grau anterior) e Visão de destino (grau atual).
        modelagem_segunda_ordem.inserir("DELETE FROM relacao_grau WHERE codigo_relacao_grau = %s;",
                                        relacao_grau_verificar)
        modelagem_segunda_ordem.inserir("INSERT INTO relacao_grau (codigo_relacao_grau, grau) VALUES (%s, %s);",
                                        (relacao_grau_verificar, relacao_grau_verificar))

        # Seleciona as Visões do Grau Anterior
        visoes_grau_anterior = modelagem_segunda_ordem.selecionar(
            """
                SELECT
                    DISTINCT visao.codigo_visao 
                FROM acesso
                INNER JOIN atributo ON atributo.codigo_atributo = acesso.codigo_atributo
                INNER JOIN visao ON visao.codigo_visao = atributo.codigo_visao
                WHERE codigo_relacao_grau = %s
            """,
            (relacao_grau_verificar - 1)
        )
        with Bar("Processando dados para Grau da Relação - Grau " + str(relacao_grau_verificar),
                 max=len(visoes_grau_anterior)) as bar_relacao_grau:
            for visao_grau_anterior in visoes_grau_anterior:
                # Seleciona na Modelagem Direta os Atributos de destino acessíveis pela Visão de origem
                visoes_acessiveis = modelagem_direta.selecionar(
                    """
                        SELECT 
                            DISTINCT codigo_visao_destino
                        FROM relacao 
                        WHERE codigo_visao_origem = %s
                    """,
                    (visao_grau_anterior["codigo_visao"])
                )
                for visao_acessivel in visoes_acessiveis:
                    # Insere os dados da Relação na tabela fato
                    modelagem_segunda_ordem.inserir(
                        """
                            INSERT IGNORE INTO acesso
                                (
                                    codigo_api_versao,
                                    codigo_autorizacao_acesso,
                                    codigo_permissao,
                                    codigo_atributo,
                                    codigo_relacao_grau,
                                    acesso
                                )
                            SELECT DISTINCT
                                codigo_api_versao,
                                codigo_autorizacao_acesso,
                                codigo_permissao,
                                atributo.codigo_atributo,
                                %s,
                                acesso
                            FROM acesso
                            INNER JOIN atributo ON atributo.codigo_atributo = acesso.codigo_atributo
                            INNER JOIN visao ON visao.codigo_visao = atributo.codigo_visao
                            WHERE
                                visao.codigo_visao = %s
                                AND codigo_relacao_grau = %s
                        """,
                        (
                            relacao_grau_verificar,
                            visao_acessivel["codigo_visao_destino"],
                            relacao_grau_verificar - 1
                        )
                    )
                bar_relacao_grau.next()
        bar_relacoes_grau.next()
