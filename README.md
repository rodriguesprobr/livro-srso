# Apresentação

Este projeto trata do material suplementar ao livro intitulado *Estruturas de Dados em Serviços de Redes Sociais Online: Uma abordagem metodológica de análise*, escrito por Fernando de Assis Rodrigues.
Aqui você encontrará códigos-fonte escritos em Python e em Structured Query Language (SQL).

O conteúdo deste projeto é de livre distribuição, desde que seja utilizada a Licença [Creative Commons 4.0 BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

## O que você precisará instalar antes de utilizar o material

Para melhor utilização dos exemplos, você precisará ter instalado os seguintes softwares
* [Python](https://www.python.org/), na versão 3 ou superior
* Sistema de Gerenciamento de Banco de Dados [MySQL](https://www.mysql.com/) ou [MariaDB](https://mariadb.org/), versões 8.0 ou superior
* [Graphviz](https://graphviz.org/), na versão 8.0 ou superior.

## O que está incluído no material suplementar

No material suplementar, está  incluido os seguintes códigos:
* Diretório/Pasta **sql**: contém os esquemas para a geração das bases de dados da Modelagem Direta e de Segunda Ordem (os quatro *Data Marts*). Os códigos podem ser aplicados nos Sistema de Gerenciamento de Banco de Dados [MySQL](https://www.mysql.com/) ou [MariaDB](https://mariadb.org/).
* Arquivo **bd.py**: este arquivo em formato Python contém em seu código-fonte a classe bd, utilizada para auxiliar  os demais arquivos em formato Python na seleção, na inserção e na exclusão de dados nas bases de dados. Necessita ter instalado a blblioteca [pymysql para o Python](https://pypi.org/project/pymysql/).
* Arquivos **exemplo_figura_31.py** e **exemplo_figura_32.py**: estes arquivos em formato Python contém em seu código-fonte os algoritmos que geram as Figuras 31 e 32 do livro. Necessitam ter instalado o Graphviz e a biblioteca [graphviz para o Python](https://pypi.org/project/graphviz/).
* Arquivos **modelagem_segunda_ordem_acesso_visao.py**, **modelagem_segunda_ordem_acesso_visao_relacao.py**, **modelagem_segunda_ordem_acesso_atributo.py** e **modelagem_segunda_ordem_acesso_atributo_relacao.py**: estes arquivos em formato Python contém em seu código-fonte os algoritmos que geram os *Data Marts* do livro. Necessitam ter instalado da biblioteca [progress para o Python](https://pypi.org/project/progress/).

Caso existam dificuldades em utilizar estes arquivos, fique à vontade para entrar em contato comigo.
