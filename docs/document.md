# Documentacao do Estudo de Caso DevSecOps

## Visao geral

Este projeto faz parte de um estudo de caso sobre criacao, implementacao e seguranca de uma aplicacao web usando conceitos de SDLC, DevOps, desenvolvimento seguro, Docker e DevSecOps.

O enunciado apresenta o tema como um sistema de pedidos de delivery, mas tambem cita uma aplicacao base de gerenciamento de tarefas pessoais. Para iniciar o trabalho pratico, foi usado o repositorio base indicado no README da atividade:

```text
https://github.com/AdityaBagad/Task-Manager-using-Flask.git
```

A aplicacao base e um sistema Flask de gerenciamento de tarefas com autenticacao de usuarios. Ela sera adaptada nas proximas etapas para atender aos requisitos do estudo de caso.

## Etapa 1 - Planejamento e requisitos

Pontos importantes solicitados no enunciado:

- definir os requisitos do sistema antes do desenvolvimento;
- separar requisitos funcionais e nao funcionais;
- criar casos de uso e fluxos do sistema;
- analisar ameacas de seguranca e medidas de mitigacao;
- definir uma arquitetura inicial com back-end e front-end.

Requisitos obrigatorios destacados no enunciado:

- a autenticacao deve ser obrigatoria antes de qualquer acao;
- a aplicacao deve gerar logs das atividades via syslog;
- o sistema deve registrar sucesso e fracasso nas autenticacoes;
- eventos de violacao de seguranca devem ser registrados nos logs.

Arquitetura exigida:

- back-end em Python com Flask;
- front-end em HTML, CSS e JavaScript;
- banco de dados para armazenar usuarios, tarefas ou pedidos;
- preparacao futura para execucao em container Docker.

## Etapa 2 - Desenvolvimento do sistema

O projeto base foi clonado e colocado diretamente na pasta:

```text
/home/docker/devsecops-delivery
```

O clone foi feito em uma pasta temporaria e depois os arquivos foram copiados para a raiz do projeto, sem manter a subpasta `Task-Manager-using-Flask`.

Arquivos e pastas principais atuais:

- `run.py`: arquivo usado para iniciar a aplicacao Flask;
- `requirements.txt`: dependencias Python do projeto;
- `todo_project/`: pacote principal da aplicacao Flask;
- `todo_project/routes.py`: rotas da aplicacao;
- `todo_project/models.py`: modelos de dados;
- `todo_project/forms.py`: formularios;
- `todo_project/templates/`: paginas HTML;
- `todo_project/static/`: arquivos CSS;
- `README.md`: README original do projeto base;
- `readme`: enunciado da atividade.

Comando para executar a aplicacao apos ativar o ambiente virtual:

```bash
source .venv/bin/activate
python run.py
```

Endereco local:

```text
http://127.0.0.1:5000
```

Containerizacao criada para a etapa 2:

- `Dockerfile`: cria a imagem da aplicacao com Python 3.12, instala as dependencias e executa o Flask na porta 5000;
- `docker-compose.yml`: sobe o servico `web`, publica a porta `5000:5000` e usa volume nomeado para persistir o SQLite;
- `.dockerignore`: impede que ambiente virtual, caches, bancos locais, Git e arquivos temporarios entrem na imagem Docker.

Comandos Docker:

```bash
docker compose build
docker compose up
docker compose up -d
curl -I http://127.0.0.1:5000/
docker compose down
docker compose down -v
```

Validacao esperada:

- build da imagem sem erro;
- aplicacao acessivel em `http://127.0.0.1:5000`;
- tela de cadastro acessivel em `http://127.0.0.1:5000/register`;
- banco SQLite criado automaticamente no volume Docker;
- ausencia do erro `no such table: user` ao cadastrar usuario.

## Problema encontrado nas dependencias

Durante a preparacao do ambiente, foi identificado um problema importante no `requirements.txt` original do projeto base.

O arquivo original continha versoes conflitantes:

```text
Flask==2.3.2
Jinja2==2.11.3
```

O problema e que `Flask==2.3.2` exige `Jinja2>=3.1.2`. Por isso, o `pip` nao conseguia instalar as dependencias ao mesmo tempo e retornava erro de conflito.

Esse problema nao parece ser proposital. Ele indica que o projeto base provavelmente esta desatualizado ou teve dependencias alteradas sem validacao completa.

Solucao aplicada:

- atualizar `Jinja2` para uma versao compativel;
- atualizar bibliotecas antigas do ecossistema Flask para versoes compativeis com Python 3.12;
- criar um ambiente virtual `.venv`;
- instalar as dependencias corrigidas dentro do ambiente virtual.

Dependencias atuais corrigidas:

```text
Flask==2.3.2
Flask-Bcrypt==1.0.1
Flask-Login==0.6.3
Flask-SQLAlchemy==3.0.5
Flask-WTF==1.2.1
WTForms==3.1.2
Jinja2==3.1.2
Werkzeug==2.3.8
```

Validacao realizada:

- o ambiente virtual `.venv` foi criado com sucesso usando `virtualenv`;
- as dependencias foram instaladas;
- o import da aplicacao Flask funcionou;
- o servidor foi iniciado com `python run.py`;
- a pagina inicial respondeu com `HTTP/1.1 200 OK`.

## Observacao sobre o ambiente Python

O comando `pip` nao estava disponivel inicialmente no sistema.

Tambem foi identificado que o `python3 -m venv` existia, mas nao conseguia criar o ambiente corretamente porque o `ensurepip` nao estava instalado no sistema.

Como nao havia permissao para instalar pacotes via `apt`, foi usada a seguinte abordagem:

- instalar `pip` no usuario;
- instalar `virtualenv`;
- criar o `.venv` com `python3 -m virtualenv .venv`;
- instalar as dependencias dentro do ambiente virtual.

Esse ponto pode ser citado no relatorio como dificuldade real de preparacao do ambiente.

## Etapa 3 - Pipeline CI/CD

O enunciado solicita a criacao de um pipeline CI/CD.

Para simplificar o ambiente e evitar consumo alto de memoria em laboratorio local, a etapa 3 foi direcionada para GitHub Actions.

Pontos que o pipeline devera contemplar:

- controle de versao com Git;
- uso de tags para marcar versoes;
- branches dedicadas para desenvolvimento, estagio e producao;
- etapa de build ou validacao da aplicacao;
- testes automatizados;
- testes unitarios, de integracao e funcionais.

Implementacao definida:

- `docker-compose.yml` permanece somente com o servico `web` da aplicacao Flask;
- o pipeline fica versionado em `.github/workflows/ci.yml`;
- o job `build` instala dependencias e valida que a aplicacao Flask pode ser importada;
- o job `sast` instala Bandit, executa analise estatica de seguranca e publica o relatorio JSON como artefato;
- a execucao acontece na nuvem, pela aba `Actions` do repositorio GitHub.

Como validar a aplicacao localmente:

```bash
docker compose up -d --build
```

Como acessar a aplicacao:

```text
http://127.0.0.1:5000
```

Como validar pelo terminal:

```bash
curl -I http://127.0.0.1:5000/
```

Como enviar para o GitHub:

```bash
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

Como acompanhar o pipeline:

- abrir o repositorio no GitHub;
- acessar a aba `Actions`;
- abrir a execucao do workflow `CI`;
- conferir os jobs `build` e `sast`;
- baixar o artefato `bandit-report`, se necessario.

Pipeline criado:

- `build`: instala dependencias e valida que a aplicacao Flask pode ser importada;
- `sast`: instala Bandit, executa `bandit -r .` e gera relatorio em `reports/bandit`.

Relatorios do Bandit:

- JSON: `reports/bandit/bandit-report.json`;
- no GitHub Actions, fica disponivel como artefato do job `sast`.

## Etapa 3.1 - Analise estatica de codigo

O enunciado solicita incluir SAST no pipeline.

Ferramentas indicadas:

- Bandit para analise estatica de seguranca em codigo Python;
- OWASP Dependency-Check para analise de dependencias vulneraveis ou desatualizadas.

Objetivo:

- identificar vulnerabilidades no codigo-fonte;
- identificar bibliotecas inseguras;
- corrigir problemas encontrados antes da entrega.

## Etapa 4 - Analise dinamica de seguranca

O enunciado solicita realizar DAST com OWASP ZAP.

Pontos importantes:

- a aplicacao deve estar em execucao;
- o ZAP deve ser iniciado a partir de uma imagem Docker;
- o scan deve apontar para a URL da aplicacao;
- o relatorio do ZAP deve ser analisado;
- problemas encontrados devem ser corrigidos e os testes repetidos.

## Etapa 4.1 - Entrega continua

O pipeline devera conter uma etapa de CD com:

- ambiente temporario de review para merge requests;
- deploy em ambiente de stage;
- validacao manual antes de producao;
- execucao de DAST no ambiente de stage.

## Etapa 7 - Feedback e monitoramento

O enunciado solicita pesquisar ferramentas capazes de monitorar logs da aplicacao e gerar alertas.

Caso importante citado:

- detectar tentativa de quebra de senha por forca bruta.

Possiveis ferramentas para analisar posteriormente:

- Fail2ban;
- Wazuh;
- Grafana com Loki;
- Prometheus com Alertmanager;
- Elastic Stack.

## Etapa 8 - Documentacao e entrega final

A entrega final deve ser um relatorio em PDF com no maximo 4 paginas.

O relatorio deve conter:

- descricao do projeto;
- etapas realizadas;
- prints das telas ou etapas mais importantes;
- ferramentas utilizadas;
- resultados alcancados;
- licoes aprendidas;
- conteudo final do arquivo `.github/workflows/ci.yml`.

Prints recomendados:

- aplicacao rodando no navegador;
- tela de login ou cadastro;
- erro/conflito inicial das dependencias, se desejado;
- ambiente virtual criado;
- pipeline CI/CD executado;
- resultado do Bandit;
- resultado do Dependency-Check;
- resultado do OWASP ZAP;
- logs ou monitoramento de autenticacao.

## Proximos passos

- adaptar a aplicacao base aos requisitos do estudo de caso;
- garantir autenticacao antes de acoes protegidas;
- implementar logs via syslog;
- registrar sucesso e falha de login;
- preparar Dockerfile e execucao em container;
- criar pipeline CI/CD;
- adicionar SAST, analise de dependencias, DAST e monitoramento.
