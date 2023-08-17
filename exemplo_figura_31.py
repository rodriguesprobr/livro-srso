#!/usr/bin/python
# -*- coding: utf8 -*-

# Importa o arquivo bd.py e a biblioteca graphviz, utilizada para gerar o Gráfico
import bd
import graphviz

# Cria um novo gráfico do tipo Digraph.
# O atributo filename estabelece onde será salvo o gráfico.
# O atributo format define que a imagem será no formato PNG.
# O atributo engine determina que o layout será dot.
# O atributo encoding define a codificação dos caracteres como UTF-8.
# O atributo node_attr determina que o formato padrão dos nós será um retângulo e a fonte será tamanho 10.
# O atributo edge_attr determina que o formato padrão das arestas será com o uso da fonte tamanho 8.
# O atributo graph_attr determina que o formato padrão do gráfico será com o uso da fonte tamanho 12, tamanho de 2048 pixels (altura e largura) e uso de arestas anguladas.
grafico = graphviz.Digraph(
    filename="C:\\Users\\usuario\\Downloads\\exemplo2",
    format="png",
    engine="dot",
    encoding="utf-8",
    node_attr={"shape":"rectangle", "fontsize":"10"},
    edge_attr={"fontsize":"8"},
    graph_attr={"fontsize":"12", "size":"2048", "splines":"ortho"}
)

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
bd.conectar(ip="", usuario="", senha="", base_dados="modelagem_direta")

# Seleciona o Serviço de Rede Social LinkedIn
servicos = bd.selecionar("""
    SELECT
        codigo_servico,
        nome
    FROM servico
    WHERE
        ativo = 1
        AND codigo_servico = 3
""")

# Iteração do Serviço
for servico in servicos:
    # Adiciona o nó do Serviço de Rede Social Online ao Gráfico, com o título formado pelo nome.
    grafico.node(
        "servico-%s" % servico["codigo_servico"],
        "Serviço de Rede Social Online\l%s" % servico["nome"]
    )

    # Seleciona as API ativas do Serviço de Rede Social
    apis = bd.selecionar("""
        SELECT 
            codigo_api,
            nome
        FROM api
        WHERE
            ativo = 1
            AND codigo_servico = %s
        """ % servico["codigo_servico"]
    )

    # Iteração das API
    for api in apis:
        # Adiciona os nós das API ao Gráfico, com o título formado pelo nome
        grafico.node(
            "api-%s" % api["codigo_api"],
            "API\l%s" % api["nome"]
        )

        # Relaciona os nós das API ao Serviço de Rede Social Online
        grafico.edge(
            "servico-%s" % servico["codigo_servico"],
            "api-%s" % api["codigo_api"],
            label="Disponbiliza"
        )

        # Seleciona as Versões da API ativas
        api_versoes = bd.selecionar("""
            SELECT
                codigo_api_versao,
                numero_versao
            FROM api_versao
            WHERE
                ativo = 1
                AND codigo_api = %s
            """ % api["codigo_api"]
        )

        # Iteração das Versões da API
        for api_versao in api_versoes:
            # Adiciona os nós das API ao Gráfico, com o título formado pelo número da versão da API
            grafico.node(
                "api_versao-%s" % api_versao["codigo_api_versao"],
                "Versão da API\l%s" % api_versao["numero_versao"]
            )

            # Relaciona os nós das Versões da API a API
            grafico.edge(
                "api-%s" % api["codigo_api"],
                "api_versao-%s" % api_versao["codigo_api_versao"],
                label="Possui"
            )

            # Seleciona as Autorizações de Acesso ativas
            autorizacoes_acesso = bd.selecionar("""
                SELECT
                    codigo_autorizacao_acesso,
                    nome
                FROM autorizacao_acesso 
                WHERE
                    ativo = 1
                    AND codigo_api = %s
                    AND codigo_api_versao = %s
                """ % (
                    api["codigo_api"],
                    api_versao["codigo_api_versao"]
                )
            )

            # Iteração das Autorizações de Acesso para a Versão da API
            for autorizacao_acesso in autorizacoes_acesso:
                # Adiciona os nós das Autorizações de Acesso ao Gráfico, com o título formado pelo nome da Autorização de Acesso
                grafico.node(
                    "autorizacao_acesso-%s" % autorizacao_acesso["codigo_autorizacao_acesso"],
                    "Autorização de Acesso\l%s" % autorizacao_acesso["nome"]
                )

                # Relaciona os nós das Autorizações de Acesso a Versão da API
                grafico.edge(
                    "api_versao-%s" % api_versao["codigo_api_versao"],
                    "autorizacao_acesso-%s" % autorizacao_acesso["codigo_autorizacao_acesso"],
                    label="Possui"
                )

            # Seleciona as Permissões ativas
            permissoes = bd.selecionar("""
                SELECT
                    codigo_permissao,
                    nome
                FROM permissao
                WHERE
                    ativo = 1
                    AND codigo_api = %s
                    AND codigo_api_versao = %s
                """ % (
                    api["codigo_api"],
                    api_versao["codigo_api_versao"]
                )
            )

            # Iteração das Permissões para a Versão da API
            for permissao in permissoes:
                # Adiciona os nós das Permissões ao Gráfico, com o título formado pelo nome da Permissão
                grafico.node(
                    "permissao-%s" % permissao["codigo_permissao"],
                    "Permissão\l%s" % permissao["nome"]
                )

            # Seleciona todas as Visões ativas relacionadas para a Versão da API que possuem relação entre si
            visoes = bd.selecionar("""
                SELECT
                    codigo_visao,
                    nome
                FROM visao 
                WHERE 
                    ativo = 1 
                    AND (
                        codigo_visao IN (SELECT codigo_visao_origem FROM relacao WHERE relacao.codigo_visao_origem = visao.codigo_visao)
                        OR
                        codigo_visao IN (SELECT codigo_visao_destino FROM relacao WHERE relacao.codigo_visao_destino = visao.codigo_visao)
                    )
                    AND codigo_api = %s
                    AND codigo_api_versao = %s
                """ % (
                    api["codigo_api"],
                    api_versao["codigo_api_versao"]
                )
            )

            # Iteração das Visões para a Versão da API
            for visao in visoes:
                # Adiciona os nós das Visões ao Gráfico, com o título formado pelo nome da Visão
                grafico.node(
                    "visao-%s" % visao["codigo_visao"],
                    "Visão\l%s" % visao["nome"]
                )

            # Seleciona as Relações das Visões para a Versão de API que estão ativas
            relacoes = bd.selecionar("""
                SELECT
                    relacao.codigo_visao_origem,
                    relacao.codigo_cardinalidade_origem,
                    c1.nome as cardinalidade_origem_nome,
                    relacao.codigo_visao_destino,
                    relacao.codigo_cardinalidade_destino,
                    c2.nome as cardinalidade_destino_nome,
                    relacao.codigo_relacao_tipo,
                    relacao.nome
                FROM relacao
                INNER JOIN cardinalidade c1 ON c1.codigo_cardinalidade = codigo_cardinalidade_origem
                INNER JOIN cardinalidade c2 ON c2.codigo_cardinalidade = codigo_cardinalidade_origem
                WHERE
                    relacao.ativo = 1
                    AND codigo_visao_origem IN (
                        SELECT
                            codigo_visao
                        FROM visao
                        WHERE
                            ativo = 1
                            AND codigo_api = %s
                            AND codigo_api_versao = %s
                    )
                    AND codigo_visao_destino IN (
                        SELECT
                            codigo_visao
                        FROM visao
                        WHERE
                            ativo = 1
                            AND codigo_api = %s
                            AND codigo_api_versao = %s
                    )
                """ % (
                    api["codigo_api"],
                    api_versao["codigo_api_versao"],
                    api["codigo_api"],
                    api_versao["codigo_api_versao"]
                )
            )

            # Iteração das Relações
            for relacao in relacoes:
                # Adiciona a relação entre as visões ao cluster. Coloca um rótulo com o título [NOME DO RELACIONAMENTO] ([CARDINALIDADE])
                grafico.edge(
                    "visao-%s" % relacao["codigo_visao_origem"],
                    "visao-%s" % relacao["codigo_visao_destino"],
                    label="Relação\l%s\l(%s-para-%s)" % (
                        relacao["nome"],
                        relacao["cardinalidade_origem_nome"],
                        relacao["cardinalidade_destino_nome"]
                    )
                )

            # Seleciona dados das Visões acessíveis pelo conjunto de Autorização de Acesso e Permissão para a Versão da API. As Visões, Autorizações de Acesso e Permissões devem estar ativas.
            autorizacao_acesso_permissao_visoes = bd.selecionar(
                """
                    SELECT
                        autorizacao_acesso_permissao_visao.codigo_autorizacao_acesso,
                        autorizacao_acesso_permissao_visao.codigo_permissao,
                        autorizacao_acesso_permissao_visao.codigo_visao,
                        visao.nome
                    FROM autorizacao_acesso_permissao_visao
                    INNER JOIN visao ON visao.codigo_visao = autorizacao_acesso_permissao_visao.codigo_visao
                    INNER JOIN autorizacao_acesso ON autorizacao_acesso.codigo_autorizacao_acesso = autorizacao_acesso_permissao_visao.codigo_autorizacao_acesso
                    INNER JOIN permissao ON permissao.codigo_permissao = autorizacao_acesso_permissao_visao.codigo_permissao
                    WHERE
                        autorizacao_acesso.ativo = 1
                        AND permissao.ativo = 1
                        AND autorizacao_acesso_permissao_visao.ativo = 1
                        AND visao.ativo = 1
                        AND autorizacao_acesso.codigo_api = %s
                        AND permissao.codigo_api = %s
                        AND autorizacao_acesso.codigo_api_versao = %s
                        AND permissao.codigo_api_versao = %s
                """ % (
                    api["codigo_api"],
                    api["codigo_api"],
                    api_versao["codigo_api_versao"],
                    api_versao["codigo_api_versao"]
                )
            )

            # Iteração das Visões para a Versão da API
            for autorizacao_acesso_permissao_visao in autorizacao_acesso_permissao_visoes:
                # Relaciona os nós das Autorizações de Acesso as Permissões
                grafico.edge(
                    "autorizacao_acesso-%s" % autorizacao_acesso_permissao_visao["codigo_autorizacao_acesso"],
                    "permissao-%s" % autorizacao_acesso_permissao_visao["codigo_permissao"],
                    label="Autoriza o acesso a"
                )

                # Relaciona os nós das Permissões as Visões
                grafico.edge(
                    "permissao-%s" % autorizacao_acesso_permissao_visao["codigo_permissao"],
                    "visao-%s" % autorizacao_acesso_permissao_visao["codigo_visao"],
                    label="Acessa a"
                )

# Renderiza o Gráfico, salvando-o de acordo com a configuração
grafico.render()

# Desconecta do Sistema Gerenciador de Banco de Dados e da Modelagem Direta
bd.desconectar()
