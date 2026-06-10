# README DevSecOps

Este projeto adapta a aplicacao Flask para um laboratorio DevSecOps com Docker, GitHub Actions, Bandit, OWASP Dependency-Check, OWASP ZAP, Prometheus e Grafana.

## Subir o Ambiente

```bash
docker compose up -d --build
```

Acessos:

- Flask: `http://localhost:5000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

Credencial padrao do Grafana:

- usuario: `admin`
- senha: `admin`

Parar o ambiente:

```bash
docker compose down
```

Remover tambem os volumes persistentes:

```bash
docker compose down -v
```

## Prometheus

O arquivo `monitoring/prometheus.yml` configura o Prometheus para coletar metricas de:

- `prometheus:9090`: metricas do proprio Prometheus.
- `web:5000/metrics`: metricas da aplicacao Flask.

A aplicacao Flask expoe `/metrics` usando `prometheus-flask-exporter`.

## Grafana

O Grafana e provisionado automaticamente com:

- datasource `Prometheus`, apontando para `http://prometheus:9090`;
- dashboard `DevSecOps Flask Observability`.

Depois de subir o ambiente, acessar:

```text
http://localhost:3000
```

Credenciais:

- usuario: `admin`
- senha: `admin`

## Bandit Local

Gerar relatorio JSON:

```bash
mkdir -p reports/bandit
.venv/bin/bandit -r . -x ./.venv,./reports -f json -o reports/bandit/bandit.json
```

Gerar relatorio TXT:

```bash
mkdir -p reports/bandit
.venv/bin/bandit -r . -x ./.venv,./reports -f txt -o reports/bandit/bandit.txt
```

Os relatorios ficam em `reports/bandit/`.

## OWASP Dependency-Check Local

Executar com Docker:

```bash
mkdir -p reports/dependency-check
docker run --rm \
  -v "$PWD:/src" \
  -v "$PWD/reports/dependency-check:/report" \
  owasp/dependency-check:latest \
  --project "DevSecOps Flask Study" \
  --scan /src \
  --out /report \
  --format HTML \
  --failOnCVSS 11
```

O relatorio HTML fica em `reports/dependency-check/`.

## OWASP ZAP Local

Subir a aplicacao:

```bash
docker compose up -d --build web
```

Executar o ZAP Baseline Scan:

```bash
mkdir -p reports/zap
docker run --rm --network host \
  -v "$PWD/reports/zap:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t http://127.0.0.1:5000 \
  -r zap-report.html \
  -w zap-report.md \
  -I
```

Os relatorios ficam em `reports/zap/`.

## GitHub Actions

O workflow `.github/workflows/devsecops.yml` executa:

- `build`: instala dependencias e valida importacao da aplicacao Flask.
- `bandit`: gera relatorios SAST em JSON e TXT.
- `dependency-check`: gera relatorio HTML de dependencias.
- `zap`: sobe a aplicacao e executa OWASP ZAP Baseline Scan.

Os jobs de seguranca foram configurados para gerar evidencia sem quebrar o pipeline apenas por achados, pois o objetivo do estudo de caso e documentar os resultados.

## Arquivos Criados ou Ajustados

- `docker-compose.yml`: adiciona Prometheus e Grafana ao ambiente Docker.
- `monitoring/prometheus.yml`: configuracao do Prometheus.
- `.github/workflows/devsecops.yml`: pipeline DevSecOps no GitHub Actions.
- `reports/bandit/`: relatorios do Bandit.
- `reports/dependency-check/`: relatorios do Dependency-Check.
- `reports/zap/`: relatorios do OWASP ZAP.
