# Objetivo

Adaptar este projeto Flask para um laboratório DevSecOps usando Docker, GitHub Actions, Bandit, OWASP Dependency-Check, OWASP ZAP, Prometheus e Grafana.

O foco é DevSecOps, não desenvolvimento da aplicação.

Não alterar a regra de negócio da aplicação.
Não refatorar templates.
Não modificar funcionalidades principais.

# Tarefas

## 1. Docker

Criar ou ajustar:

* `Dockerfile`
* `docker-compose.yml`

O `docker-compose.yml` deve subir:

* aplicação Flask
* Prometheus
* Grafana

Portas esperadas:

* Flask: `5000`
* Prometheus: `9090`
* Grafana: `3000`

Criar volumes persistentes para Prometheus e Grafana.

## 2. Prometheus

Criar a pasta:

```text
monitoring/
```

Criar o arquivo:

```text
monitoring/prometheus.yml
```

Configurar o Prometheus para monitorar os serviços disponíveis no ambiente.

Caso a aplicação Flask não exponha métricas nativamente, deixar configurado ao menos o Prometheus funcionando e documentar que métricas da aplicação exigiriam exporter ou endpoint `/metrics`.

## 3. GitHub Actions

Criar o workflow:

```text
.github/workflows/devsecops.yml
```

O pipeline deve conter:

* checkout do código
* setup do Python
* instalação das dependências
* validação básica da aplicação
* Bandit
* OWASP Dependency-Check
* OWASP ZAP Baseline Scan

## 4. Bandit

Executar análise SAST com Bandit.

Gerar relatório em:

```text
reports/bandit/
```

Formatos desejados:

```text
bandit.json
bandit.txt
```

O pipeline não deve quebrar apenas por encontrar achados de segurança, pois o objetivo é gerar evidência para relatório acadêmico.

## 5. OWASP Dependency-Check

Executar análise de dependências com OWASP Dependency-Check.

Gerar relatório em:

```text
reports/dependency-check/
```

Formato desejado:

```text
HTML
```

O pipeline deve salvar o relatório como artifact.

## 6. OWASP ZAP

Executar OWASP ZAP Baseline Scan contra a aplicação Flask em execução.

Target esperado:

```text
http://localhost:5000
```

Gerar relatório em:

```text
reports/zap/
```

Formatos desejados:

```text
zap-report.html
zap-report.md
```

O pipeline não deve quebrar apenas por alertas encontrados, pois o objetivo é gerar evidência para o estudo de caso.

Referência: o ZAP Baseline Scan executa uma varredura passiva e rápida contra a aplicação em execução.

## 7. Estrutura esperada

Organizar o projeto para ficar assim:

```text
project/
├── .github/
│   └── workflows/
│       └── devsecops.yml
├── monitoring/
│   └── prometheus.yml
├── reports/
│   ├── bandit/
│   ├── dependency-check/
│   └── zap/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## 8. Documentação

Atualizar ou criar um `README_DEVSECOPS.md` contendo:

* Como subir a aplicação com Docker Compose
* Como acessar Flask, Prometheus e Grafana
* Como executar Bandit localmente
* Como executar Dependency-Check localmente
* Como executar OWASP ZAP localmente
* Como visualizar os relatórios gerados
* Explicação curta dos arquivos criados

## Resultado esperado

Ao final, o projeto deve permitir:

```bash
docker compose up -d
```

E acessar:

```text
Flask: http://localhost:5000
Prometheus: http://localhost:9090
Grafana: http://localhost:3000
```

Também deve existir um workflow do GitHub Actions executando:

```text
Build
Bandit
Dependency-Check
OWASP ZAP
```

com relatórios salvos como artifacts para uso no relatório final do estudo de caso.
