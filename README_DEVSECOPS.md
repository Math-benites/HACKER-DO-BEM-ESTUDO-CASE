# README DevSecOps

Este projeto adapta a aplicacao Flask para um laboratorio DevSecOps com Docker, GitHub Actions, Bandit, OWASP Dependency-Check, OWASP ZAP, Prometheus e Grafana.

## Subir o Ambiente

```bash
docker compose up -d --build
```

Acessos:

- Aplicacao via Nginx: `http://localhost:5000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Loki: `http://localhost:3100`

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

## Nginx, Rate Limit, Loki e Fail2Ban

O servico `nginx` fica na frente do Flask e publica a aplicacao em `http://localhost:5000`.
O Flask continua no servico interno `web:5000`.

O Nginx aplica rate limit em:

- `/login`: limite de tentativas de autenticacao;
- `/register`: limite de tentativas de cadastro;
- demais rotas: limite geral contra excesso de requisicoes.

Os logs sao persistidos em volumes Docker e coletados pelo `promtail`:

- logs do Nginx com label `job="nginx"`;
- logs da aplicacao Flask com label `job="flask"` e `app="task-manager"`;
- logs do Fail2Ban com label `job="fail2ban"`.

O Fail2Ban monitora:

- respostas `429` no access log do Nginx;
- eventos `event=login_failure` gerados pela aplicacao.

Para gerar evidencias de rate limit:

```bash
for i in $(seq 1 20); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5000/login; done
```

Para consultar logs no Loki:

```bash
curl -G http://localhost:3100/loki/api/v1/query \
  --data-urlencode 'query={job="nginx"}'
```

```bash
curl -G http://localhost:3100/loki/api/v1/query \
  --data-urlencode 'query={app="task-manager"} |= "event=login_failure"'
```

Se o teste gerar um ban no Fail2Ban para o IP interno do Docker, remover o ban:

```bash
docker compose exec fail2ban fail2ban-client set nginx-rate-limit unbanip 172.18.0.1
```

## Grafana

O Grafana e provisionado automaticamente com:

- datasource `Prometheus`, apontando para `http://prometheus:9090`;
- datasource `Loki`, apontando para `http://loki:3100`;
- dashboard `DevSecOps Flask Observability`.

Depois de subir o ambiente, acessar:

```text
http://localhost:3000
```

Credenciais:

- usuario: `admin`
- senha: `admin`

Dashboard principal:

```text
http://localhost:3000/d/devsecops-flask-observability/devsecops-flask-observability
```

O dashboard contem as secoes:

- Visao Geral;
- Flask;
- Autenticacao e Seguranca;
- Rate Limit;
- Syslog e Logs;
- Fail2Ban.

O painel `Flask Requests por Segundo` usa Prometheus e funciona com as metricas atuais da aplicacao. Os paineis de `Rate Limit`, `Syslog` e `Fail2Ban` usam Loki e sao alimentados pelos logs coletados pelo Promtail.

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

- `docker-compose.yml`: adiciona Flask, Nginx, Prometheus, Loki, Promtail, Fail2Ban e Grafana ao ambiente Docker.
- `monitoring/nginx/default.conf`: reverse proxy e rate limit.
- `monitoring/prometheus.yml`: configuracao do Prometheus.
- `monitoring/promtail/config.yml`: coleta logs do Nginx, Flask e Fail2Ban para o Loki.
- `monitoring/fail2ban/`: jails e filtros do Fail2Ban.
- `monitoring/grafana/dashboards/flask-observability.json`: dashboard com metricas Flask, rate limit, syslog e Fail2Ban.
- `.github/workflows/devsecops.yml`: pipeline DevSecOps no GitHub Actions.
- `reports/bandit/`: relatorios do Bandit.
- `reports/dependency-check/`: relatorios do Dependency-Check.
- `reports/zap/`: relatorios do OWASP ZAP.
