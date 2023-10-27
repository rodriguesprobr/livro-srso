-- Gera o esquema da Modelagem Direta para o Sistema Gerenciador de Banco de Dados MySQL/MariaDB
-- Autor: Fernando de Assis Rodrigues
-- Copyright: 2023 - Fernando de Assis Rodrigues
-- Crédito: Fernando de Assis Rodrigues
-- Licença: Creative Commons 4.0 BY-SA-ND
-- Versão: 1.0
-- Mantenedor: Fernando de Assis Rodrigues
-- E-mail: fernando@rodrigues.pro.br
-- Status: Produção
--
-- Informações sobre a exportação:
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 27-Out-2023 às 23:25
-- Versão do servidor: 10.4.28-MariaDB
-- versão do PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `modelagem_direta`
--
CREATE DATABASE IF NOT EXISTS `modelagem_direta` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `modelagem_direta`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `api`
--

CREATE TABLE `api` (
  `codigo_api` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_servico` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre Serviço de Rede Social Online e Application Programming Interface, com origem na tabela servico, campo codigo_servico.',
  `nome` text NOT NULL COMMENT 'O nome da Application Programming Interface.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que contém as informações sobre cada Application Programming Interface.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `api_versao`
--

CREATE TABLE `api_versao` (
  `codigo_api_versao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_api` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Application Programming Interface e a Versão da Application Programming Interface, com origem na tabela api, campo codigo_api.',
  `numero_versao` varchar(200) NOT NULL COMMENT 'Número da Versão da Application Programming Interface.',
  `data_lancamento` date NOT NULL COMMENT 'Data de início do funcionamento da Versão da Application Programming Interface.',
  `data_descontinuidade` date DEFAULT NULL COMMENT 'Data do encerramento da disponibildiade da Versão da Application Programming Interface.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Versão da Application Programming Interface (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O principal endereço de acesso ao documento da Versão da Application Programming Interface, no formato Uniform Resource Locator.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Versão de Application Programming Interface.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `atributo`
--

CREATE TABLE `atributo` (
  `codigo_atributo` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_visao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Visão e o Atributo, com origem na tabela visao, campo codigo_visao.',
  `codigo_dado_tipo` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Atributo e o Tipo de Dado para os seus valores, com origem na tabela dado_tipo, campo codigo_dado_tipo.',
  `codigo_dado_valor` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Atributo e o Valor de Dado para os seus valores, com origem na tabela dado_valor, campo codigo_dado_valor.',
  `nome` varchar(200) NOT NULL COMMENT 'Nome original do Atributo, conforme descrito na documentação de referência.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original do Atributo (quando disponível), conforme documentação de referência.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Atributo disponível nas Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `atributo_qualificador`
--

CREATE TABLE `atributo_qualificador` (
  `codigo_atributo` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Atributo e o Qualificador, com origem na tabela atributo, campo codigo_atributo.',
  `codigo_qualificador` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Atributo e o Qualificador, com origem na tabela qualificador, campo codigo_qualificador.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade associativa de união entre Atributos e Qualificadores. Utilizada para relacionar quais são os Qualificadores de cada Atributo.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `autorizacao_acesso`
--

CREATE TABLE `autorizacao_acesso` (
  `codigo_autorizacao_acesso` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_api` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Application Programming Interface e a Autorização de Acesso, com origem na tabela api_versao, campo codigo_api.',
  `codigo_api_versao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Versão da Application Programming Interface e a Autorização de Acesso, com origem na tabela api_versao, campo codigo_versao_api.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome da Autorização de Acesso.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Autorização de Acesso (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O endereço principal de acesso ao documento da Autorização de Acesso, no formato Uniform Resource Locator.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Autorização de Acesso.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `autorizacao_acesso_atributo`
--

CREATE TABLE `autorizacao_acesso_atributo` (
  `codigo_autorizacao_acesso` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso e o Atributo, com origem na tabela autorizacao_acesso, campo codigo_autorizacao_acesso.',
  `codigo_atributo` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso e o Atributo, com origem na tabela atributo, campo codigo_atributo.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade associativa de união entre Autorizações de Acesso e Atributos. Utilizada para relacionar quais Atributos estão disponíveis em cada Autorização de Acesso.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `autorizacao_acesso_permissao_atributo`
--

CREATE TABLE `autorizacao_acesso_permissao_atributo` (
  `codigo_autorizacao_acesso` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso, a Permissão e o Atributo, com origem na tabela autorizacao_acesso, campo codigo_autorizacao_acesso.',
  `codigo_permissao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso, a Permissão e o Atributo, com origem na tabela permissao, campo codigo_permissao.',
  `codigo_atributo` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso, a Permissão e o Atributo, com origem na tabela atributo, campo codigo_atributo.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade associativa de união entre Autorizações de Acesso, Permissões e Atributos. Utilizada para relacionar quais Atributos estão disponíveis com o uso de Autorização de Acesso e Permissão.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `autorizacao_acesso_permissao_visao`
--

CREATE TABLE `autorizacao_acesso_permissao_visao` (
  `codigo_autorizacao_acesso` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso, a Permissão e a Visão, com origem na tabela autorizacao_acesso, campo codigo_autorizacao_acesso.',
  `codigo_permissao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso, a Permissão e a Visão, com origem na tabela permissao, campo codigo_permissao.',
  `codigo_visao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso, a Permissão e a Visão, com origem na tabela visao, campo codigo_visao.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade associativa de união entre Autorizações de Acesso, Permissões e Visões. Utilizada para relacionar quais Visões estão disponíveis com o uso de Autorização de Acesso e Permissão.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `autorizacao_acesso_visao`
--

CREATE TABLE `autorizacao_acesso_visao` (
  `codigo_autorizacao_acesso` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso e a Visão, com origem na tabela autorizacao_acesso, campo codigo_autorizacao_acesso.',
  `codigo_visao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Autorização de Acesso e a Visão, com origem na tabela visao, campo codigo_autorizacao_acesso.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade associativa de união entre Autorizações de Acesso e Visões. Utilizada para relacionar quais Visões estão disponíveis em cada Autorização de Acesso.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `cardinalidade`
--

CREATE TABLE `cardinalidade` (
  `codigo_cardinalidade` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` char(6) NOT NULL COMMENT 'O nome da Cardinalidade, podendo ser 1-para-1, 1-para-N ou N-para-N.',
  `descricao` text NOT NULL COMMENT 'A descrição das Cardinalidades: 1-para-1, 1-para-N ou N-para-N.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Tabela Auxiliar utilizada para armazenar dados que descrevem as Cardinalidades das Relações entre as Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `coletor`
--

CREATE TABLE `coletor` (
  `codigo_coletor` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome completo do coletor.',
  `email` varchar(2048) NOT NULL COMMENT 'O endereço de e-mail do coletor.',
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'A data de criação de cada registro da tabela, gerado automaticamente.',
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'A data de criação de cada registro da tabela, gerado automaticamente na inserção. O seu valor deve ser alterado para o valor padrão CURRENT_TIMESTAMP no caso do registro ser alterado.',
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre os membros da equipe que coletarão os dados sobre os Serviços de Redes Sociais Oniline.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `dado_formato`
--

CREATE TABLE `dado_formato` (
  `codigo_dado_formato` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome do formato que os dados podem ser coletados.',
  `descricao` text NOT NULL COMMENT 'A descrição do formato que os dados podem ser coletados.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Tabela Auxiliar utilizada para armazenar dados que descrevem os Formatos de Dados disponíveis no momento da coleta de dados por meio das Requisições.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `dado_tipo`
--

CREATE TABLE `dado_tipo` (
  `codigo_dado_tipo` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` text NOT NULL COMMENT 'O nome do Tipo de Dado.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição das características do Tipo de Dado.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Tabela Auxiliar utilizada para armazenar dados que descrevem os Tipos de Dados utilizados por Atributos das Visões ou por Parâmetros das Requisições.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `dado_valor`
--

CREATE TABLE `dado_valor` (
  `codigo_dado_valor` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome do Valor de Dado esperado para cada dado.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição das características do Valor de Dado esperado para cada dado.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Tabela Auxiliar utilizada para armazenar dados que descrevem os Valores de Dados utilizados por Atributos das Visões ou por Parâmetros das Requisições.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `parametro`
--

CREATE TABLE `parametro` (
  `codigo_parametro` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_dado_tipo` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Parâmetro e o Tipo de Dado para os seus valores, com origem na tabela dado_tipo, campo codigo_parametro.',
  `codigo_dado_valor` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Parâmetro e o Valor de Dado para os seus valores, com origem na tabela dado_valor, campo codigo_dado_valor.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome do Parâmetro.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original do Parâmetro (quando disponível), conforme documentação de referência.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Parâmetro disponível nas Requisições.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `parametro_qualificador`
--

CREATE TABLE `parametro_qualificador` (
  `codigo_parametro` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Parâmetro e o Qualificador, com origem na tabela parametro, campo codigo_parametro.',
  `codigo_qualificador` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Parâmetro e o Qualificador, com origem na tabela qualificador, campo codigo_qualificador.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade associativa de união entre Parâmetros e Qualificadores. Utilizada para relacionar quais são os Qualificadores de cada Parâmetro.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `permissao`
--

CREATE TABLE `permissao` (
  `codigo_permissao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_api` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Application Programming Interface e a Permissão, com origem na tabela api_versao, campo codigo_api.',
  `codigo_api_versao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Versão da Application Programming Interface e a Permissão, com origem na tabela api_versao, campo codigo_versao_api.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome da Permissão.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Permissão (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O endereço de acesso da documentação contendo a referência da Permissão, no formato Uniform Resource Locator.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Permissão.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `qualificador`
--

CREATE TABLE `qualificador` (
  `codigo_qualificador` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(200) NOT NULL COMMENT 'Nome original do Qualificador, conforme descrito na documentação de referência.',
  `descricao` text NOT NULL COMMENT 'A descrição original do Qualificador (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O endereço principal de acesso ao documento do qualificador, no formato Uniform Resource Locator.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Qualificador.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `relacao`
--

CREATE TABLE `relacao` (
  `codigo_relacao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_visao_origem` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Relacionamento e a Visão de origem, com origem na tabela visao, campo id.',
  `codigo_cardinalidade_origem` int(11) NOT NULL COMMENT 'A Cardinalidade do relacionamento com a Visão de origem.',
  `codigo_visao_destino` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Relacionamento e a Visão de destino, com origem na tabela visao, campo id.',
  `codigo_cardinalidade_destino` int(11) NOT NULL COMMENT 'A Cardinalidade do relacionamento com a Visão de destino.',
  `codigo_relacao_tipo` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre o Relacionamento e o Tipo de Relacionamento entre as Visões, com origem na tabela tipo_relacao, campo id.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome do relacionamento.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Relação entre as Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `relacao_tipo`
--

CREATE TABLE `relacao_tipo` (
  `codigo_relaciao_tipo` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(20) NOT NULL COMMENT 'O nome do Tipo de Relação entre as Visões.',
  `descricao` text NOT NULL COMMENT 'Descrição sobre as características do Tipo de Relação entre as Visões.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Tabela Auxiliar utilizada para armazenar dados que descrevem os Tipos de Relacionamentos entre as Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `requisicao`
--

CREATE TABLE `requisicao` (
  `codigo_requisicao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_visao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Requisição e a Visão, com origem na tabela visao, campo codigo_visao.',
  `codigo_dado_formato` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Requisição e o Formato do Dado, com origem na tabela dado_formato, campo codigo_dado_formato.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome da Requisição.',
  `protocolo` text NOT NULL COMMENT 'Nome do protocolo utilizado para realizar a requisição e coletar os dados.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Requisição (quando disponível), conforme documentação de referência.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Requisição.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `requisicao_parametro`
--

CREATE TABLE `requisicao_parametro` (
  `codigo_requisicao` int(11) NOT NULL DEFAULT 0 COMMENT 'Chave estrangeira do relacionamento entre a Requisição e o Parâmetro, com origem na tabela requisicao, campo codigo_requisicao.',
  `codigo_parametro` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Requisição e o Parâmetro, com origem na tabela parametro, campo codigo_parametro.',
  `direcao` varchar(7) NOT NULL COMMENT 'Sentido do parâmetro no momento da requisição. Ele pode ser de entrada, de saída, de entrada e saída.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade associativa de união entre Requisições e Parâmetros. Utilizada para relacionar quais são os Parâmetros de cada Requisição.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `servico`
--

CREATE TABLE `servico` (
  `codigo_servico` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` text NOT NULL COMMENT 'O nome do Serviço de Rede Social Online.',
  `url` text NOT NULL COMMENT 'O principal endereço de acesso ao Serviço de Rede Social Online, no formato Uniform Resource Locator.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre os Serviços de Redes Sociais Online aos quais as Application Programming Interfaces estão vinculadas.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `visao`
--

CREATE TABLE `visao` (
  `codigo_visao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_api` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Application Programming Interface e a Visão, com origem na tabela api_versao, campo codigo_api.',
  `codigo_api_versao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a Versão da Application Programming Interface e a Visão, com origem na tabela api_versao, campo codigo_api_versao.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome original da Visão, conforme descrito na documentação de referência.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Visão (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O principal endereço de acesso ao documento da Visão, no formato Uniform Resource Locator.',
  `codigo_coletor` int(11) NOT NULL,
  `data_criacao` datetime NOT NULL DEFAULT current_timestamp(),
  `data_modificacao` datetime NOT NULL DEFAULT current_timestamp(),
  `ativo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Entidade que armazena dados sobre cada Visão.';

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `api`
--
ALTER TABLE `api`
  ADD PRIMARY KEY (`codigo_api`),
  ADD KEY `fk_api_origem_idx` (`codigo_servico`),
  ADD KEY `fk_api_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `api_versao`
--
ALTER TABLE `api_versao`
  ADD PRIMARY KEY (`codigo_api_versao`,`codigo_api`),
  ADD UNIQUE KEY `version_number_UNIQUE` (`numero_versao`),
  ADD KEY `fk_api_has_versao_api1_idx` (`codigo_api`),
  ADD KEY `fk_api_versao_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `atributo`
--
ALTER TABLE `atributo`
  ADD PRIMARY KEY (`codigo_atributo`),
  ADD KEY `fk_coluna_visao1_idx` (`codigo_visao`),
  ADD KEY `fk_coluna_tipo_dado1_idx` (`codigo_dado_tipo`),
  ADD KEY `fk_column_data_value1_idx` (`codigo_dado_valor`),
  ADD KEY `fk_atributo_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `atributo_qualificador`
--
ALTER TABLE `atributo_qualificador`
  ADD PRIMARY KEY (`codigo_atributo`,`codigo_qualificador`),
  ADD KEY `fk_coluna_has_qualificador_qualificador1_idx` (`codigo_qualificador`),
  ADD KEY `fk_coluna_has_qualificador_coluna1_idx` (`codigo_atributo`),
  ADD KEY `fk_atributo_qualificador_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `autorizacao_acesso`
--
ALTER TABLE `autorizacao_acesso`
  ADD PRIMARY KEY (`codigo_autorizacao_acesso`),
  ADD KEY `fk_autorizacao_api_versao1_idx` (`codigo_api_versao`,`codigo_api`),
  ADD KEY `fk_autorizacao_acesso_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `autorizacao_acesso_atributo`
--
ALTER TABLE `autorizacao_acesso_atributo`
  ADD PRIMARY KEY (`codigo_autorizacao_acesso`,`codigo_atributo`),
  ADD KEY `fk_autorizacao_coluna_coluna1_idx` (`codigo_atributo`),
  ADD KEY `fk_autorizacao_acesso_atributo_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `autorizacao_acesso_permissao_atributo`
--
ALTER TABLE `autorizacao_acesso_permissao_atributo`
  ADD PRIMARY KEY (`codigo_autorizacao_acesso`,`codigo_permissao`,`codigo_atributo`),
  ADD KEY `fk_autorizacao_permissao_coluna_permissao1_idx` (`codigo_permissao`),
  ADD KEY `fk_autorizacao_permissao_coluna_coluna1_idx` (`codigo_atributo`),
  ADD KEY `fk_autorizacao_acesso_permissao_atributo_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `autorizacao_acesso_permissao_visao`
--
ALTER TABLE `autorizacao_acesso_permissao_visao`
  ADD PRIMARY KEY (`codigo_autorizacao_acesso`,`codigo_permissao`,`codigo_visao`),
  ADD KEY `fk_autorizacao_permissao_visao_permissao1_idx` (`codigo_permissao`),
  ADD KEY `fk_autorizacao_permissao_visao_visao1_idx` (`codigo_visao`),
  ADD KEY `fk_autorizacao_acesso_permissao_visao_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `autorizacao_acesso_visao`
--
ALTER TABLE `autorizacao_acesso_visao`
  ADD PRIMARY KEY (`codigo_autorizacao_acesso`,`codigo_visao`),
  ADD KEY `fk_autorizacao_visao_visao1_idx` (`codigo_visao`),
  ADD KEY `fk_autorizacao_acesso_visao_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `cardinalidade`
--
ALTER TABLE `cardinalidade`
  ADD PRIMARY KEY (`codigo_cardinalidade`),
  ADD KEY `fk_cardinalidade_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `coletor`
--
ALTER TABLE `coletor`
  ADD PRIMARY KEY (`codigo_coletor`);

--
-- Índices para tabela `dado_formato`
--
ALTER TABLE `dado_formato`
  ADD PRIMARY KEY (`codigo_dado_formato`),
  ADD KEY `fk_dado_formato_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `dado_tipo`
--
ALTER TABLE `dado_tipo`
  ADD PRIMARY KEY (`codigo_dado_tipo`),
  ADD KEY `fk_dado_tipo_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `dado_valor`
--
ALTER TABLE `dado_valor`
  ADD PRIMARY KEY (`codigo_dado_valor`),
  ADD UNIQUE KEY `name_UNIQUE` (`nome`),
  ADD KEY `fk_dado_valor_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `parametro`
--
ALTER TABLE `parametro`
  ADD PRIMARY KEY (`codigo_parametro`),
  ADD KEY `fk_parametro_tipo_dado1_idx` (`codigo_dado_tipo`),
  ADD KEY `fk_parameter_data_value1_idx` (`codigo_dado_valor`),
  ADD KEY `fk_parametro_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `parametro_qualificador`
--
ALTER TABLE `parametro_qualificador`
  ADD PRIMARY KEY (`codigo_parametro`,`codigo_qualificador`),
  ADD KEY `fk_parametro_has_qualificador_qualificador1_idx` (`codigo_qualificador`),
  ADD KEY `fk_parametro_has_qualificador_parametro1_idx` (`codigo_parametro`),
  ADD KEY `fk_parametro_qualificador_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `permissao`
--
ALTER TABLE `permissao`
  ADD PRIMARY KEY (`codigo_permissao`),
  ADD UNIQUE KEY `name_UNIQUE` (`nome`),
  ADD KEY `fk_permissao_api_versao1_idx` (`codigo_api_versao`,`codigo_api`),
  ADD KEY `fk_permissao_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `qualificador`
--
ALTER TABLE `qualificador`
  ADD PRIMARY KEY (`codigo_qualificador`),
  ADD KEY `fk_qualificador_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `relacao`
--
ALTER TABLE `relacao`
  ADD PRIMARY KEY (`codigo_relacao`),
  ADD KEY `fk_relacao_visao1_idx` (`codigo_visao_origem`),
  ADD KEY `fk_relacao_visao2_idx` (`codigo_visao_destino`),
  ADD KEY `fk_relacao_cardinalidade1_idx` (`codigo_cardinalidade_origem`),
  ADD KEY `fk_relacao_cardinalidade2_idx` (`codigo_cardinalidade_destino`),
  ADD KEY `fk_relacao_tipo_relacao1_idx` (`codigo_relacao_tipo`),
  ADD KEY `fk_relacao_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `relacao_tipo`
--
ALTER TABLE `relacao_tipo`
  ADD PRIMARY KEY (`codigo_relaciao_tipo`),
  ADD UNIQUE KEY `name_UNIQUE` (`nome`),
  ADD KEY `fk_relacionamento_tipo_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `requisicao`
--
ALTER TABLE `requisicao`
  ADD PRIMARY KEY (`codigo_requisicao`),
  ADD KEY `fk_requisicao_visao1_idx` (`codigo_visao`),
  ADD KEY `fk_requisicao_formato_dados1_idx` (`codigo_dado_formato`),
  ADD KEY `fk_requisicao_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `requisicao_parametro`
--
ALTER TABLE `requisicao_parametro`
  ADD PRIMARY KEY (`codigo_requisicao`,`codigo_parametro`),
  ADD KEY `fk_requisicao_has_parametro_parametro1_idx` (`codigo_parametro`),
  ADD KEY `fk_requisicao_has_parametro_requisicao1_idx` (`codigo_requisicao`),
  ADD KEY `fk_requisicao_parametro_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `servico`
--
ALTER TABLE `servico`
  ADD PRIMARY KEY (`codigo_servico`),
  ADD KEY `fk_servico_coletor1_idx` (`codigo_coletor`);

--
-- Índices para tabela `visao`
--
ALTER TABLE `visao`
  ADD PRIMARY KEY (`codigo_visao`),
  ADD KEY `fk_visao_api_versao1_idx` (`codigo_api_versao`,`codigo_api`),
  ADD KEY `fk_visao_coletor1_idx` (`codigo_coletor`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `api`
--
ALTER TABLE `api`
  MODIFY `codigo_api` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `api_versao`
--
ALTER TABLE `api_versao`
  MODIFY `codigo_api_versao` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `atributo`
--
ALTER TABLE `atributo`
  MODIFY `codigo_atributo` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `autorizacao_acesso`
--
ALTER TABLE `autorizacao_acesso`
  MODIFY `codigo_autorizacao_acesso` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `coletor`
--
ALTER TABLE `coletor`
  MODIFY `codigo_coletor` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `dado_formato`
--
ALTER TABLE `dado_formato`
  MODIFY `codigo_dado_formato` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `dado_tipo`
--
ALTER TABLE `dado_tipo`
  MODIFY `codigo_dado_tipo` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `dado_valor`
--
ALTER TABLE `dado_valor`
  MODIFY `codigo_dado_valor` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `parametro`
--
ALTER TABLE `parametro`
  MODIFY `codigo_parametro` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `permissao`
--
ALTER TABLE `permissao`
  MODIFY `codigo_permissao` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `qualificador`
--
ALTER TABLE `qualificador`
  MODIFY `codigo_qualificador` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `relacao`
--
ALTER TABLE `relacao`
  MODIFY `codigo_relacao` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `requisicao`
--
ALTER TABLE `requisicao`
  MODIFY `codigo_requisicao` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `servico`
--
ALTER TABLE `servico`
  MODIFY `codigo_servico` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- AUTO_INCREMENT de tabela `visao`
--
ALTER TABLE `visao`
  MODIFY `codigo_visao` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.';

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `api`
--
ALTER TABLE `api`
  ADD CONSTRAINT `fk_api_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_api_origem` FOREIGN KEY (`codigo_servico`) REFERENCES `servico` (`codigo_servico`);

--
-- Limitadores para a tabela `api_versao`
--
ALTER TABLE `api_versao`
  ADD CONSTRAINT `fk_api_has_versao_api1` FOREIGN KEY (`codigo_api`) REFERENCES `api` (`codigo_api`),
  ADD CONSTRAINT `fk_api_versao_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `atributo`
--
ALTER TABLE `atributo`
  ADD CONSTRAINT `fk_atributo_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_column_data_value1` FOREIGN KEY (`codigo_dado_valor`) REFERENCES `dado_valor` (`codigo_dado_valor`),
  ADD CONSTRAINT `fk_coluna_tipo_dado1` FOREIGN KEY (`codigo_dado_tipo`) REFERENCES `dado_tipo` (`codigo_dado_tipo`),
  ADD CONSTRAINT `fk_coluna_visao1` FOREIGN KEY (`codigo_visao`) REFERENCES `visao` (`codigo_visao`);

--
-- Limitadores para a tabela `atributo_qualificador`
--
ALTER TABLE `atributo_qualificador`
  ADD CONSTRAINT `fk_atributo_qualificador_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_coluna_has_qualificador_coluna1` FOREIGN KEY (`codigo_atributo`) REFERENCES `atributo` (`codigo_atributo`),
  ADD CONSTRAINT `fk_coluna_has_qualificador_qualificador1` FOREIGN KEY (`codigo_qualificador`) REFERENCES `qualificador` (`codigo_qualificador`);

--
-- Limitadores para a tabela `autorizacao_acesso`
--
ALTER TABLE `autorizacao_acesso`
  ADD CONSTRAINT `fk_autorizacao_acesso_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_autorizacao_api_versao1` FOREIGN KEY (`codigo_api_versao`,`codigo_api`) REFERENCES `api_versao` (`codigo_api_versao`, `codigo_api`);

--
-- Limitadores para a tabela `autorizacao_acesso_atributo`
--
ALTER TABLE `autorizacao_acesso_atributo`
  ADD CONSTRAINT `fk_autorizacao_acesso_atributo_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_autorizacao_coluna_autorizacao1` FOREIGN KEY (`codigo_autorizacao_acesso`) REFERENCES `autorizacao_acesso` (`codigo_autorizacao_acesso`),
  ADD CONSTRAINT `fk_autorizacao_coluna_coluna1` FOREIGN KEY (`codigo_atributo`) REFERENCES `atributo` (`codigo_atributo`);

--
-- Limitadores para a tabela `autorizacao_acesso_permissao_atributo`
--
ALTER TABLE `autorizacao_acesso_permissao_atributo`
  ADD CONSTRAINT `fk_autorizacao_acesso_permissao_atributo_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_autorizacao_permissao_coluna_autorizacao1` FOREIGN KEY (`codigo_autorizacao_acesso`) REFERENCES `autorizacao_acesso` (`codigo_autorizacao_acesso`),
  ADD CONSTRAINT `fk_autorizacao_permissao_coluna_coluna1` FOREIGN KEY (`codigo_atributo`) REFERENCES `atributo` (`codigo_atributo`),
  ADD CONSTRAINT `fk_autorizacao_permissao_coluna_permissao1` FOREIGN KEY (`codigo_permissao`) REFERENCES `permissao` (`codigo_permissao`);

--
-- Limitadores para a tabela `autorizacao_acesso_permissao_visao`
--
ALTER TABLE `autorizacao_acesso_permissao_visao`
  ADD CONSTRAINT `fk_autorizacao_acesso_permissao_visao_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_autorizacao_permissao_visao_autorizacao1` FOREIGN KEY (`codigo_autorizacao_acesso`) REFERENCES `autorizacao_acesso` (`codigo_autorizacao_acesso`),
  ADD CONSTRAINT `fk_autorizacao_permissao_visao_permissao1` FOREIGN KEY (`codigo_permissao`) REFERENCES `permissao` (`codigo_permissao`),
  ADD CONSTRAINT `fk_autorizacao_permissao_visao_visao1` FOREIGN KEY (`codigo_visao`) REFERENCES `visao` (`codigo_visao`);

--
-- Limitadores para a tabela `autorizacao_acesso_visao`
--
ALTER TABLE `autorizacao_acesso_visao`
  ADD CONSTRAINT `fk_autorizacao_acesso_visao_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_autorizacao_visao_autorizacao1` FOREIGN KEY (`codigo_autorizacao_acesso`) REFERENCES `autorizacao_acesso` (`codigo_autorizacao_acesso`),
  ADD CONSTRAINT `fk_autorizacao_visao_visao1` FOREIGN KEY (`codigo_visao`) REFERENCES `visao` (`codigo_visao`);

--
-- Limitadores para a tabela `cardinalidade`
--
ALTER TABLE `cardinalidade`
  ADD CONSTRAINT `fk_cardinalidade_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `dado_formato`
--
ALTER TABLE `dado_formato`
  ADD CONSTRAINT `fk_dado_formato_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `dado_tipo`
--
ALTER TABLE `dado_tipo`
  ADD CONSTRAINT `fk_dado_tipo_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `dado_valor`
--
ALTER TABLE `dado_valor`
  ADD CONSTRAINT `fk_dado_valor_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `parametro`
--
ALTER TABLE `parametro`
  ADD CONSTRAINT `fk_parameter_data_value1` FOREIGN KEY (`codigo_dado_valor`) REFERENCES `dado_valor` (`codigo_dado_valor`),
  ADD CONSTRAINT `fk_parametro_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_parametro_tipo_dado1` FOREIGN KEY (`codigo_dado_tipo`) REFERENCES `dado_tipo` (`codigo_dado_tipo`);

--
-- Limitadores para a tabela `parametro_qualificador`
--
ALTER TABLE `parametro_qualificador`
  ADD CONSTRAINT `fk_parametro_has_qualificador_parametro1` FOREIGN KEY (`codigo_parametro`) REFERENCES `parametro` (`codigo_parametro`),
  ADD CONSTRAINT `fk_parametro_has_qualificador_qualificador1` FOREIGN KEY (`codigo_qualificador`) REFERENCES `qualificador` (`codigo_qualificador`),
  ADD CONSTRAINT `fk_parametro_qualificador_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `permissao`
--
ALTER TABLE `permissao`
  ADD CONSTRAINT `fk_permissao_api_versao1` FOREIGN KEY (`codigo_api_versao`,`codigo_api`) REFERENCES `api_versao` (`codigo_api_versao`, `codigo_api`),
  ADD CONSTRAINT `fk_permissao_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `qualificador`
--
ALTER TABLE `qualificador`
  ADD CONSTRAINT `fk_qualificador_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `relacao`
--
ALTER TABLE `relacao`
  ADD CONSTRAINT `fk_relacao_cardinalidade1` FOREIGN KEY (`codigo_cardinalidade_origem`) REFERENCES `cardinalidade` (`codigo_cardinalidade`),
  ADD CONSTRAINT `fk_relacao_cardinalidade2` FOREIGN KEY (`codigo_cardinalidade_destino`) REFERENCES `cardinalidade` (`codigo_cardinalidade`),
  ADD CONSTRAINT `fk_relacao_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_relacao_tipo_relacao1` FOREIGN KEY (`codigo_relacao_tipo`) REFERENCES `relacao_tipo` (`codigo_relaciao_tipo`),
  ADD CONSTRAINT `fk_relacao_visao1` FOREIGN KEY (`codigo_visao_origem`) REFERENCES `visao` (`codigo_visao`),
  ADD CONSTRAINT `fk_relacao_visao2` FOREIGN KEY (`codigo_visao_destino`) REFERENCES `visao` (`codigo_visao`);

--
-- Limitadores para a tabela `relacao_tipo`
--
ALTER TABLE `relacao_tipo`
  ADD CONSTRAINT `fk_relacionamento_tipo_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `requisicao`
--
ALTER TABLE `requisicao`
  ADD CONSTRAINT `fk_requisicao_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`),
  ADD CONSTRAINT `fk_requisicao_formato_dados1` FOREIGN KEY (`codigo_dado_formato`) REFERENCES `dado_formato` (`codigo_dado_formato`),
  ADD CONSTRAINT `fk_requisicao_visao1` FOREIGN KEY (`codigo_visao`) REFERENCES `visao` (`codigo_visao`);

--
-- Limitadores para a tabela `requisicao_parametro`
--
ALTER TABLE `requisicao_parametro`
  ADD CONSTRAINT `fk_requisicao_has_parametro_parametro1` FOREIGN KEY (`codigo_parametro`) REFERENCES `parametro` (`codigo_parametro`),
  ADD CONSTRAINT `fk_requisicao_has_parametro_requisicao1` FOREIGN KEY (`codigo_requisicao`) REFERENCES `requisicao` (`codigo_requisicao`),
  ADD CONSTRAINT `fk_requisicao_parametro_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `servico`
--
ALTER TABLE `servico`
  ADD CONSTRAINT `fk_servico_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

--
-- Limitadores para a tabela `visao`
--
ALTER TABLE `visao`
  ADD CONSTRAINT `fk_visao_api_versao1` FOREIGN KEY (`codigo_api_versao`,`codigo_api`) REFERENCES `api_versao` (`codigo_api_versao`, `codigo_api`),
  ADD CONSTRAINT `fk_visao_coletor1` FOREIGN KEY (`codigo_coletor`) REFERENCES `coletor` (`codigo_coletor`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
