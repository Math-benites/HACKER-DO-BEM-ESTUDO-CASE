# Etapa 3 - Pipeline CI/CD no GitHub

## Objetivo

Configurar o pipeline CI/CD usando GitHub Actions, mantendo a aplicacao Flask em Docker e sem alterar a regra de negocio do projeto.

## Decisao

O laboratorio local de CI/CD foi removido para simplificar o ambiente. A etapa 3 passa a usar GitHub na nuvem, com workflow versionado no repositorio.

## Arquivos

- `.github/workflows/ci.yml`: workflow de CI/CD.
- `docker-compose.yml`: permanece somente com o servico `web` da aplicacao Flask.
- `reports/bandit/`: caminho usado para relatorios locais, quando necessario.

## Pipeline

O workflow possui dois jobs:

- `build`: faz checkout, configura Python 3.12, instala dependencias e valida importacao da aplicacao Flask.
- `sast`: instala Bandit, executa analise estatica de seguranca e publica o relatorio JSON como artefato.

## Como usar

Criar um repositorio no GitHub e enviar este projeto:

```bash
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

Depois do push:

- abrir o repositorio no GitHub;
- acessar a aba `Actions`;
- abrir a execucao do workflow `CI`;
- conferir os jobs `build` e `sast`;
- baixar o artefato `bandit-report`, se necessario.

## Validacao Local da Aplicacao

Subir a aplicacao:

```bash
docker compose up -d --build
```

Validar:

```bash
curl -I http://127.0.0.1:5000/
```

Parar:

```bash
docker compose down
```

## Resultado Esperado

- Aplicacao Flask continua funcionando em Docker.
- Pipeline executa automaticamente a cada `push` ou `pull_request`.
- Job `build` valida que o projeto instala e importa corretamente.
- Job `sast` executa Bandit e disponibiliza o relatorio como artefato.
