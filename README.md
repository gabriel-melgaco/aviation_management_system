# SGE — Sistema de Gestão de Estoque de Aviação

Sistema de gerenciamento de estoque e pedidos desenvolvido para o **Batalhão de Aviação do Exército**. Permite controle completo de inventário de peças aeronáuticas, rastreamento de pedidos de manutenção e movimentação de materiais.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12 / Django 5.2 |
| Banco de dados (produção) | PostgreSQL 15 |
| Banco de dados (desenvolvimento) | SQLite3 |
| Servidor WSGI | Gunicorn |
| Proxy reverso | Nginx (Alpine) |
| Containerização | Docker / Docker Compose |
| Planilhas | openpyxl 3.1.5 |
| Frontend | Django Templates + Bootstrap + Chart.js + Select2 |
| Variáveis de ambiente | python-dotenv |
| Linting | flake8 |

---

## Funcionalidades

### Inventário
- Cadastro de itens com MPN, PN e documentação técnica
- Controle de estoque por localização física (OM, seção, prateleira, estojo)
- Rastreamento de número de série
- Classificação por tipo Kanban (Motor, Célula, Padrão)
- Alertas de quantidade mínima e vencimento
- Importação em lote via planilha Excel

### Pedidos
- Tipos de pedido: **RMS** (manutenção), **FSM** (apoio), **REQ** (requisição)
- Ciclo de vida completo: `Não Aberto → Aberto → Em Andamento → Fechado → Encerrado / Cancelado`
- Classificação de urgência: **RUSH**, **PROG**, **AOG**
- Vinculação a aeronave (origem e destino), TSN e TSO de componentes
- Rastreamento de documentos técnicos (TEC PUB, DPE, EGLOG)
- Controle de nota fiscal (NF) e cartão de log
- Exportação de pedidos para Excel
- Importação de contratos RMS/FSM via planilha

### Movimentação
- Registro de **entradas** (inflow) com rastreamento de usuário e data
- Registro de **saídas** (outflow) com motivo e seção solicitante

### Dashboard
- Métricas em tempo real: total de itens, pedidos abertos, itens abaixo do mínimo
- Gráficos de entradas e saídas dos últimos 7 dias (Chart.js)
- Distribuição de status de pedidos
- Filtragem por período (mês/ano)

### Segurança e Auditoria
- Autenticação nativa do Django com controle de permissões por view
- Registro de `criado_por` e `atualizado_por` em todas as operações
- Restrição de deleção de registros referenciados

---

## Estrutura do Projeto

```
sge/
├── app/                  # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── views.py          # Dashboard
│   ├── metrics.py        # Cálculos de métricas
│   └── templates/
├── aircraft/             # Cadastro de aeronaves
├── inventory/            # Gestão de estoque
├── item/                 # Catálogo de peças
├── location/             # Localizações físicas
├── order/                # Pedidos de manutenção
├── inflow/               # Entradas de material
├── outflow/              # Saídas de material
├── reports/              # Módulo de relatórios
├── static/               # CSS, JS, imagens, planilhas modelo
├── nginx/                # Configuração do Nginx
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Configuração e Execução

### Pré-requisitos
- Docker e Docker Compose instalados

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DJANGO_ENV=prd           # dev ou prd
DEBUG=False
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=sge
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha-segura
POSTGRES_HOST=sge_db
POSTGRES_PORT=5432
```

### Subir com Docker

```bash
docker compose up -d --build
```

Acesse em: `http://localhost`

### Desenvolvimento local (sem Docker)

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar banco de desenvolvimento (SQLite)
echo "DJANGO_ENV=dev" > .env

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

---

## Importação de Dados

O sistema disponibiliza comandos para importação em lote via planilha Excel:

```bash
# Importar inventário de prateleira
python manage.py prateleira_import

# Importar inventário Kanban de motores
python manage.py kanban_motor_import

# Importar pedidos de contrato RMS
python manage.py pedidos_contrato_RMS

# Importar pedidos de contrato FSM
python manage.py pedidos_contrato_FSM
```

Modelos de planilha disponíveis em `static/spreadsheet/`.

---

## Licença

Uso interno — Batalhão de Aviação do Exército.
