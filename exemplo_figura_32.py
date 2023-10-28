#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Este script gera a Figura 32, utilizada no livro.

É necessário ter instalado o aplicativo Graphviz: https://graphviz.org/download/
Utiliza a classe bd do arquivo bd.py para realizar a conexão com o Sistema Gerenciador do Banco de Dados MySQL/MariaDB.
"""
import graphviz  # Importa a biblioteca graphviz, utilizada para gerar o Gráfico
from bd import bd  # Importa a classe bd do arquivo bd.py

__author__ = "Fernando de Assis Rodrigues"
__copyright__ = "2023 - Fernando de Assis Rodrigues"
__credits__ = ["Fernando de Assis Rodrigues"]
__license__ = "Creative Commons 4.0 BY-NC-SA"
__version__ = "1.0"
__maintainer__ = "Fernando de Assis Rodrigues"
__email__ = "fernando@rodrigues.pro.br"
__status__ = "Produção"

"""Cria um novo gráfico do tipo Digraph.
O atributo filename estabelece onde será salvo o gráfico.
O atributo format define que a imagem será no formato PNG.
O atributo engine determina que o layout será dot.
O atributo encoding define a codificação dos caracteres como UTF-8.
O atributo node_attr determina que o formato padrão dos nós será do tipo record, similar as Entidades do 
Diagrama Entidade-Relacionamento e a fonte será tamanho 10.
O atributo edge_attr determina que o formato padrão das arestas será com o uso da fonte tamanho 8.
O atributo graph_attr determina que o formato padrão do gráfico será com o uso da fonte tamanho 12, 
tamanho de 2048 pixels (altura e largura) e uso de arestas anguladas.
"""
grafico = graphviz.Digraph(
    filename="C:\\Users\\usuario\\Downloads\\exemplo32",  # Personalizar
    format="png",
    engine="dot",
    encoding="utf-8",
    node_attr={"shape": "record", "fontsize": "10"},
    edge_attr={"fontsize": "8"},
    graph_attr={"fontsize": "40", "splines": "ortho"}
)

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
# Personalizar as informações ip, usuario, senha e base_dados de acordo com a instalação do MySQL/MariaDB
modelagem_direta = bd(ip="localhost", usuario="usuario_do_banco_de_dados", senha="senha", base_dados="modelagem_direta")

# Seleciona as Versões de API que estão ativas
api_versoes = modelagem_direta.selecionar("""
    SELECT
        codigo_api_versao,
        nome,
        numero_versao
    FROM api_versao
    INNER JOIN api ON api.codigo_api = api_versao.codigo_api
    WHERE
        api_versao.ativo = %s
""", 1)
# Iteração das Versões de API
for api_versao in api_versoes:
    # Cria um cluster para cada Versão de API
    with grafico.subgraph(name="cluster_%s" % api_versao["codigo_api_versao"]) as cluster:
        # Estabelece como rótulo do cluster, com título formado pelo nome e a versão da API
        cluster.attr(label="%s (%s)" % (
            api_versao["nome"],
            api_versao["numero_versao"]
        ))
        # Ajusta o alinhamento do rótulo do cluster para a esquerda.
        cluster.attr(labeljust="l")
        # Seleciona as Visões da Versão de API que estão ativas
        visoes = modelagem_direta.selecionar("""
            SELECT
                codigo_visao,
                nome
            FROM visao
            WHERE
                visao.ativo = %s
                AND
                codigo_api_versao = %s
            """, (1, api_versao["codigo_api_versao"]))
        # Iteração das Visões
        for visao in visoes:
            # Seleciona os Atributos da Visão que estão ativos
            atributos = modelagem_direta.selecionar("""
                SELECT
                    nome
                FROM atributo 
                WHERE
                    ativo = %s
                    AND codigo_visao = %s
                """, (1, visao["codigo_visao"]))
            # Cria uma variável node_atributos, que receberá todos os atributos da visão para serem exibidos
            node_atributos = ""
            # Iteração dos Atributos
            for atributo in atributos:
                # Adiciona o nome de cada atributo a variável node_atributos, seguido de uma quebra de linha \l
                node_atributos += "%s\\l" % atributo["nome"]
            # Adiciona o nó ao cluster
            cluster.node(
                str(visao["codigo_visao"]),
                "{%s|%s}" % (
                    visao["nome"],
                    node_atributos
                )
            )
        # Seleciona as Relações das Visões para a Versão de API que estão ativas
        relacoes = modelagem_direta.selecionar("""
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
                relacao.ativo = %s
                AND codigo_visao_origem IN (
                    SELECT
                        codigo_visao
                    FROM visao
                    WHERE codigo_api_versao = %s
                )
            """, (1, api_versao["codigo_api_versao"]))
        # Iteração das Relações
        for relacao in relacoes:
            # Adiciona a relação entre as visões ao cluster.
            # Coloca um rótulo com o título [NOME DO RELACIONAMENTO] ([CARDINALIDADE])
            cluster.edge(
                str(relacao["codigo_visao_origem"]),
                str(relacao["codigo_visao_destino"]),
                label="%s (%s-para-%s)" % (
                    relacao["nome"],
                    relacao["cardinalidade_origem_nome"],
                    relacao["cardinalidade_destino_nome"]
                )
            )
# Renderiza o Gráfico, salvando-o de acordo com a configuração
grafico.render()
# Desconecta do Sistema Gerenciador de Banco de Dados e da Modelagem Direta
modelagem_direta.desconectar()
