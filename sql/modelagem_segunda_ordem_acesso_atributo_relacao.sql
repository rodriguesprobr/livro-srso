-- Gera o esquema da Modelagem de Segunda Ordem - Quarto Data Mart
-- para o Sistema Gerenciador de Banco de Dados MySQL/MariaDB
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
-- Tempo de geração: 27-Out-2023 às 23:35
-- Versão do servidor: 10.4.28-MariaDB
-- versão do PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `modelagem_segunda_ordem_acesso_atributo_relacao`
--
CREATE DATABASE IF NOT EXISTS `modelagem_segunda_ordem_acesso_atributo_relacao` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `modelagem_segunda_ordem_acesso_atributo_relacao`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `acesso`
--

CREATE TABLE `acesso` (
  `codigo_api_versao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a dimensão Versão da Application Programming Interface e a tabela fato de acesso as Visões, com origem na tabela api_versao, campo codigo_api_versao.',
  `codigo_autorizacao_acesso` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a dimensão Autorização de Acesso e a tabela fato de acesso as Visões, com origem na tabela autorizacao_acesso, campo codigo_autorizacao_acesso.',
  `codigo_permissao` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a dimensão Permissão e a tabela fato de acesso as Visões, com origem na tabela permissao, campo codigo_permissao.',
  `codigo_atributo` int(11) NOT NULL COMMENT 'Chave estrangeira do relacionamento entre a dimensão Atributo e a tabela fato de acesso as Visões, com origem na tabela atributo, campo codigo_atributo',
  `codigo_relacao_grau` int(11) NOT NULL,
  `acesso` tinyint(4) NOT NULL COMMENT 'O valor do atributo acesso representará se quais são os Atributos estão disponíveis para acesso pela combinação entre o conjunto Versão da Application Programming Interface, Autorização de Acesso e Permissão. Opcionalmente, o coletor poderá adicionar a consulta dados de a) um determinado Atributo, por meio da dimensão Atributo, b) um determinado Tipo de Dado para o Atributo, por meio da dimensão Tipo de Dado, c) um determinada Visão para o Atributo, por meio da dimensão Visão, d) uma determinada Application Programming Interface, por meio da dimensão Application Programming Interface, e e) um determinardo Serviço de Rede Social Online, por meio da dimensão Serviços de Redes Sociais Online.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabela Fato, intitulada acesso, que representará as diversas combinações possíveis de acesso às Visões, combinando dados dos Serviços de Redes Sociais Online, Application Programming Interfaces, Versões das Application Programming Interfaces, Autorizações de Acesso, Permissões e Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `api`
--

CREATE TABLE `api` (
  `codigo_api` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_servico` int(11) NOT NULL,
  `nome` text NOT NULL COMMENT 'O nome da Application Programming Interface.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre as Application Programming Interfaces que estão vinculados às Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `api_versao`
--

CREATE TABLE `api_versao` (
  `codigo_api_versao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_api` int(11) NOT NULL,
  `numero_versao` varchar(200) NOT NULL COMMENT 'Número da Versão da Application Programming Interface.',
  `data_lancamento` date NOT NULL COMMENT 'Data de início do funcionamento da Versão da Application Programming Interface.',
  `data_descontinuidade` date DEFAULT NULL COMMENT 'Data do encerramento da disponibildiade da Versão da Application Programming Interface.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Versão da Application Programming Interface (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O principal endereço de acesso ao documento da Versão da Application Programming Interface, no formato Uniform Resource Locator.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre as Versões das Application Programming Interfaces que estão vinculados às Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `atributo`
--

CREATE TABLE `atributo` (
  `codigo_atributo` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `codigo_dado_tipo` int(11) NOT NULL,
  `codigo_visao` int(11) NOT NULL,
  `nome` varchar(200) NOT NULL COMMENT 'Nome original do Atributo, conforme descrito na documentação de referência.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original do Atributo (quando disponível), conforme documentação de referência.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre os Atributos acessíveis pela Modelagem Direta.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `autorizacao_acesso`
--

CREATE TABLE `autorizacao_acesso` (
  `codigo_autorizacao_acesso` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome da Autorização de Acesso.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Autorização de Acesso (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O endereço principal de acesso ao documento da Autorização de Acesso, no formato Uniform Resource Locator.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre as Autorizações de Acesso que dão acesso às Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `dado_tipo`
--

CREATE TABLE `dado_tipo` (
  `codigo_dado_tipo` int(11) NOT NULL,
  `nome` varchar(200) NOT NULL COMMENT 'O nome do Tipo de Dado.',
  `descricao` varchar(200) DEFAULT NULL COMMENT 'A descrição das características do Tipo de Dado.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre os Tipos de Dados dos Atributos acessíveis pela Modelagem Direta.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `permissao`
--

CREATE TABLE `permissao` (
  `codigo_permissao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome da Permissão.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Permissão (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O endereço de acesso da documentação contendo a referência da Permissão, no formato Uniform Resource Locator.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre as Permissões que dão acesso às Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `relacao_grau`
--

CREATE TABLE `relacao_grau` (
  `codigo_relacao_grau` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `grau` int(11) NOT NULL COMMENT 'Grau da relação. O Valor 1 representa que o Atributo é acessível por meio de uma Visão que está diretamente por uma Autorização de Acesso ou um conjunto entre Autorização de Acesso e Permissão. Valores acima de 1 representam que o atributo é acessível por meio da relação de sua Visão com outra Visão, na modalidade Visão de Origem --> Visão de Destino. Quão maior o número, mais Relações são necessárias para acessar o Atributo.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre os possíveis graus de Relação entre Atributos por meio das Visões. O Valor 1 representa que o Atributo é acessível por meio de uma Visão que está diretamente por uma Autorização de Acesso ou um conjunto entre Autorização de Acesso e Permissão. Valores acima de 1 representam que o atributo é acessível por meio da relação de sua Visão com outra Visão, na modalidade Visão de Origem --> Visão de Destino. Quão maior o número, mais Relações são necessárias para acessar o Atributo.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `servico`
--

CREATE TABLE `servico` (
  `codigo_servico` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` text NOT NULL COMMENT 'O nome do Serviço de Rede Social Online.',
  `url` text NOT NULL COMMENT 'O principal endereço de acesso ao Serviço de Rede Social Online, no formato Uniform Resource Locator.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre os Serviços de Redes Sociais que estão vinculados às Visões.';

-- --------------------------------------------------------

--
-- Estrutura da tabela `visao`
--

CREATE TABLE `visao` (
  `codigo_visao` int(11) NOT NULL COMMENT 'Chave primária e artificial da tabela, gerada automaticamente.',
  `nome` varchar(200) NOT NULL COMMENT 'O nome original da Visão, conforme descrito na documentação de referência.',
  `descricao` text DEFAULT NULL COMMENT 'A descrição original da Visão (quando disponível), conforme documentação de referência.',
  `url` text NOT NULL COMMENT 'O principal endereço de acesso ao documento da Visão, no formato Uniform Resource Locator.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Entidade que armazena dados sobre a dimensão que representará um ponto de acesso para consultas sobre as Visões acessíveis pela Modelagem Direta.';

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `acesso`
--
ALTER TABLE `acesso`
  ADD PRIMARY KEY (`codigo_api_versao`,`codigo_autorizacao_acesso`,`codigo_permissao`,`codigo_atributo`,`codigo_relacao_grau`),
  ADD KEY `fk_acesso_atributo1` (`codigo_atributo`),
  ADD KEY `fk_acesso_autorizacao_acesso1` (`codigo_autorizacao_acesso`),
  ADD KEY `fk_acesso_permissao1` (`codigo_permissao`),
  ADD KEY `fk_acesso_relacao_grau1` (`codigo_relacao_grau`);

--
-- Índices para tabela `api`
--
ALTER TABLE `api`
  ADD PRIMARY KEY (`codigo_api`),
  ADD KEY `fk_api_servico1` (`codigo_servico`);

--
-- Índices para tabela `api_versao`
--
ALTER TABLE `api_versao`
  ADD PRIMARY KEY (`codigo_api_versao`),
  ADD KEY `fk_api_versao_api` (`codigo_api`);

--
-- Índices para tabela `atributo`
--
ALTER TABLE `atributo`
  ADD PRIMARY KEY (`codigo_atributo`),
  ADD KEY `fk_atributo_dado_tipo1` (`codigo_dado_tipo`),
  ADD KEY `fk_atributo_visao1` (`codigo_visao`);

--
-- Índices para tabela `autorizacao_acesso`
--
ALTER TABLE `autorizacao_acesso`
  ADD PRIMARY KEY (`codigo_autorizacao_acesso`);

--
-- Índices para tabela `dado_tipo`
--
ALTER TABLE `dado_tipo`
  ADD PRIMARY KEY (`codigo_dado_tipo`);

--
-- Índices para tabela `permissao`
--
ALTER TABLE `permissao`
  ADD PRIMARY KEY (`codigo_permissao`);

--
-- Índices para tabela `relacao_grau`
--
ALTER TABLE `relacao_grau`
  ADD PRIMARY KEY (`codigo_relacao_grau`);

--
-- Índices para tabela `servico`
--
ALTER TABLE `servico`
  ADD PRIMARY KEY (`codigo_servico`);

--
-- Índices para tabela `visao`
--
ALTER TABLE `visao`
  ADD PRIMARY KEY (`codigo_visao`);

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `acesso`
--
ALTER TABLE `acesso`
  ADD CONSTRAINT `fk_acesso_api_versao1` FOREIGN KEY (`codigo_api_versao`) REFERENCES `api_versao` (`codigo_api_versao`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_acesso_atributo1` FOREIGN KEY (`codigo_atributo`) REFERENCES `atributo` (`codigo_atributo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_acesso_autorizacao_acesso1` FOREIGN KEY (`codigo_autorizacao_acesso`) REFERENCES `autorizacao_acesso` (`codigo_autorizacao_acesso`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_acesso_permissao1` FOREIGN KEY (`codigo_permissao`) REFERENCES `permissao` (`codigo_permissao`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_acesso_relacao_grau1` FOREIGN KEY (`codigo_relacao_grau`) REFERENCES `relacao_grau` (`codigo_relacao_grau`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `api`
--
ALTER TABLE `api`
  ADD CONSTRAINT `fk_api_servico1` FOREIGN KEY (`codigo_servico`) REFERENCES `servico` (`codigo_servico`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `api_versao`
--
ALTER TABLE `api_versao`
  ADD CONSTRAINT `fk_api_versao_api` FOREIGN KEY (`codigo_api`) REFERENCES `api` (`codigo_api`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `atributo`
--
ALTER TABLE `atributo`
  ADD CONSTRAINT `fk_atributo_dado_tipo1` FOREIGN KEY (`codigo_dado_tipo`) REFERENCES `dado_tipo` (`codigo_dado_tipo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_atributo_visao1` FOREIGN KEY (`codigo_visao`) REFERENCES `visao` (`codigo_visao`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
