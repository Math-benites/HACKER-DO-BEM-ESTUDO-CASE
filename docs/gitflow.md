# GitFlow do Projeto

Este documento define o fluxo de branches usado no estudo de caso DevSecOps.
O objetivo e organizar o desenvolvimento, correcoes e entregas mantendo rastreabilidade no GitHub.

## Branches Principais

### main

Branch principal do projeto.
Representa a versao estavel e pronta para entrega.

Regras:

- deve receber apenas codigo validado;
- deve receber merge via Pull Request;
- deve disparar o pipeline DevSecOps;
- deve conter versoes demonstraveis do estudo de caso.

### develop

Branch de integracao.
Recebe funcionalidades antes de irem para `main`.

Regras:

- concentra as alteracoes em andamento;
- recebe merges de `feature/*` e `bugfix/*`;
- deve passar no pipeline antes de abrir PR para `main`.

## Branches de Trabalho

### feature/*

Usada para novas funcionalidades.

Exemplos neste projeto:

- `feature/docker-flask`
- `feature/github-actions`
- `feature/prometheus-grafana`
- `feature/nginx-rate-limit`
- `feature/loki-fail2ban`

Comandos:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/nginx-rate-limit
```

Finalizacao:

```bash
git push origin feature/nginx-rate-limit
```

Depois abrir Pull Request para `develop`.

### bugfix/*

Usada para corrigir problemas encontrados durante desenvolvimento ou pipeline.

Exemplos neste projeto:

- `bugfix/audit-log-path-ci`
- `bugfix/zap-nginx-port`
- `bugfix/sqlite-create-tables`

Comandos:

```bash
git checkout develop
git pull origin develop
git checkout -b bugfix/zap-nginx-port
```

Finalizacao:

```bash
git push origin bugfix/zap-nginx-port
```

Depois abrir Pull Request para `develop`.

### hotfix/*

Usada para correcao urgente em producao ou na branch `main`.
Parte da `main` e volta para `main` e `develop`.

Exemplo:

- `hotfix/pipeline-main-failing`

Comandos:

```bash
git checkout main
git pull origin main
git checkout -b hotfix/pipeline-main-failing
```

Finalizacao:

```bash
git push origin hotfix/pipeline-main-failing
```

Depois abrir Pull Request para `main` e replicar a correcao para `develop`.

### release/*

Usada para preparar uma entrega.
Permite ajustes finais de documentacao, versao e validacoes.

Exemplo:

- `release/v1-devsecops-case`

Comandos:

```bash
git checkout develop
git pull origin develop
git checkout -b release/v1-devsecops-case
```

Finalizacao:

```bash
git push origin release/v1-devsecops-case
```

Depois abrir Pull Request para `main`.

## Fluxo Recomendado

1. Criar a branch `develop` a partir da `main`.
2. Criar branches `feature/*` para novas etapas do estudo.
3. Criar branches `bugfix/*` para corrigir falhas do pipeline ou da aplicacao.
4. Abrir Pull Request para `develop`.
5. Validar GitHub Actions.
6. Criar `release/*` quando a entrega estiver pronta.
7. Abrir Pull Request da release para `main`.
8. Criar tag da versao final.

## Exemplo Completo

```bash
git checkout main
git pull origin main
git checkout -b develop
git push origin develop

git checkout -b feature/loki-fail2ban
git add .
git commit -m "Add Loki and Fail2Ban observability"
git push origin feature/loki-fail2ban
```

Depois:

- abrir Pull Request de `feature/loki-fail2ban` para `develop`;
- aguardar pipeline DevSecOps;
- revisar evidencias;
- aprovar e fazer merge.

## Pipeline DevSecOps no GitFlow

O GitHub Actions deve rodar em:

- push em qualquer branch;
- Pull Request para `develop`;
- Pull Request para `main`.

Validacoes esperadas:

- build da aplicacao Flask;
- importacao da aplicacao;
- Bandit;
- OWASP Dependency-Check;
- OWASP ZAP;
- evidencias de observabilidade quando aplicavel.

## Padrao de Commits

Padrao simples recomendado:

```text
Add Docker containerization
Fix CI audit log path
Update Grafana dashboard
Document GitFlow process
```

Para evidencias do estudo de caso, cada commit deve representar uma etapa clara.

## Tags

Ao finalizar uma entrega:

```bash
git checkout main
git pull origin main
git tag -a v1.0-devsecops-case -m "DevSecOps case study delivery"
git push origin v1.0-devsecops-case
```

## Resumo Visual

```text
main
  ^
  |
release/v1-devsecops-case
  ^
  |
develop
  ^          ^
  |          |
feature/*  bugfix/*

hotfix/* sai de main e retorna para main e develop
```
