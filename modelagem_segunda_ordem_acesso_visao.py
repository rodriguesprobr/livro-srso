#!/usr/bin/python
# -*- coding: utf8 -*-

from bd import bd

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem Direta
modelagem_direta = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_segunda_ordem_acesso_visao")

# Conecta no Sistema Gerenciador de Banco de Dados, na Modelagem de Segunda Ordem - Acesso Visão
modelagem_segunda_ordem = bd(ip="localhost", usuario="root", senha="", base_dados="modelagem_segunda_ordem_acesso_visao")

# Exclui dados das dimensões para refrescamento e atualização
estado = modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.servico;")
print(estado)
estado = modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.api;")
estado = modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.api_versao;")
estado = modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.autorizacao_acesso;")
estado = modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.permissao;")
estado = modelagem_segunda_ordem.executar("DELETE FROM modelagem_segunda_ordem_acesso_visao.visao;")


'''/* Insere dados para a dimensão serviço, a partir da tabela servico da Modelagem Direta, filtrando somente valores ativos */
INSERT INTO modelagem_segunda_ordem_acesso_visao.servico (codigo_servico, nome, url)
SELECT codigo_servico, nome, url FROM modelagem_direta.servico
WHERE ativo = 1;
/* Insere dados para a dimensão api, a partir da tabela api da Modelagem Direta, filtrando somente valores ativos */
INSERT INTO modelagem_segunda_ordem_acesso_visao.api (codigo_api, nome)
SELECT codigo_api, nome FROM modelagem_direta.api
WHERE ativo = 1;
/* Insere dados para a dimensão api_versao, a partir da tabela api_versao da Modelagem Direta, filtrando somente valores ativos */
INSERT INTO modelagem_segunda_ordem_acesso_visao.api_versao (codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url)
SELECT codigo_api_versao, numero_versao, data_lancamento, data_descontinuidade, descricao, url FROM modelagem_direta.api_versao
WHERE ativo = 1;
/* Insere dados para a dimensão autorizacao_acesso, a partir da tabela autorizacao_acesso da Modelagem Direta, filtrando somente valores ativos */
INSERT INTO modelagem_segunda_ordem_acesso_visao.autorizacao_acesso (codigo_autorizacao_acesso, nome, descricao, url)
SELECT codigo_autorizacao_acesso, nome, descricao, url FROM modelagem_direta.autorizacao_acesso
WHERE ativo = 1;
/* Insere dados para a dimensão permissao, a partir da tabela permissao da Modelagem Direta, filtrando somente valores ativos */
INSERT INTO modelagem_segunda_ordem_acesso_visao.permissao (codigo_permissao, nome, descricao, url)
SELECT codigo_permissao, nome, descricao, url FROM modelagem_direta.permissao
WHERE ativo = 1;
/* Insere dados para a dimensão visao, a partir da tabela permissao da Modelagem Direta, filtrando somente valores ativos */
INSERT INTO modelagem_segunda_ordem_acesso_visao.visao (codigo_visao, nome, descricao, url)
SELECT codigo_visao, nome, descricao, url FROM modelagem_direta.visao
WHERE ativo = 1;'''