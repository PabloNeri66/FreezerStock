# FreezerStock (OSLO Gelados) - README

Projeto Django simples para gerenciar geladinhos (produtos), entradas (inflows) e saídas (outflows).

Visão geral
- App principal: gerenciamento de produtos ("geladinhos") e controle de estoque através de entradas e saídas.
- Métricas de estoque e vendas calculadas em [`core/metrics.py`](core/metrics.py) via as funções [`core.metrics.get_geladinho_metrics`](core/metrics.py) e [`core.metrics.get_sales_metrics`](core/metrics.py).

Arquitetura / arquivos importantes
- Configuração do projeto: [core/settings.py](core/settings.py) e [manage.py](manage.py)
- URLs principais: [core/urls.py](core/urls.py) (inclui [geladinhos/urls.py](geladinhos/urls.py), [inflows/urls.py](inflows/urls.py) e [outflows/urls.py](outflows/urls.py))
- Models:
  - [`geladinhos.models.Geladinho`](geladinhos/models.py) — modelo de produto ([geladinhos/models.py](geladinhos/models.py))
  - [`inflows.models.Inflow`](inflows/models.py) — entradas de estoque ([inflows/models.py](inflows/models.py))
  - [`outflows.models.Outflow`](outflows/models.py) — saídas de estoque ([outflows/models.py](outflows/models.py))
- Forms: [geladinhos/forms.py](geladinhos/forms.py), [inflows/forms.py](inflows/forms.py), [outflows/forms.py](outflows/forms.py)
- Signals que atualizam o estoque automaticamente:
  - [`inflows.signals.update_geladinho_quantity`](inflows/signals.py) ([inflows/signals.py](inflows/signals.py))
  - [`outflows.signals.update_geladinho_quantity`](outflows/signals.py) ([outflows/signals.py](outflows/signals.py))
- Templates base e componentes: [core/templates/base.html](core/templates/base.html) e [core/templates/components/_*.html](core/templates/components/)
- Views que expõem listas/criar/detalhes: [geladinhos/views.py](geladinhos/views.py), [inflows/views.py](inflows/views.py), [outflows/views.py](outflows/views.py)
- Banco de dados: A Configurar, utilzei Postgres.

Instalação (rápido)
1. Criar e ativar virtualenv:
   - Ex.: python -m venv .venv && source .venv/bin/activate (Linux/macOS) ou .venv\Scripts\activate (Windows)
2. Instalar dependências:
   - pip install -r requirements.txt (adicione um requirements se necessário)
3. Configurar variáveis de ambiente (ex.: `.env`) usadas por [core/settings.py](core/settings.py) (SECRET_KEY, DEBUG, DB_HOST, DB_PASSWORD, ...)

Banco de dados / migrações
- Usar as migrations já presentes em cada app (ex.: [geladinhos/migrations](geladinhos/migrations/), [inflows/migrations](inflows/migrations/), [outflows/migrations](outflows/migrations/)) para criar tabelas.
- Comandos comuns:
  - python manage.py makemigrations
  - python manage.py migrate

Executando localmente
- Iniciar servidor de desenvolvimento:
  - python manage.py runserver
- Acesse:
  - Dashboard / lista de geladinhos via as rotas definidas em [geladinhos/urls.py](geladinhos/urls.py), [inflows/urls.py](inflows/urls.py) e [outflows/urls.py](outflows/urls.py). A homepage é servida por [core/views.py::home](core/views.py) e configurada em [core/urls.py](core/urls.py).

Observações rápidas
- As métricas mostradas nas views usam [`core.metrics.get_geladinho_metrics`](core/metrics.py) e [`core.metrics.get_sales_metrics`](core/metrics.py) — útil para dashboard.
- Signals atualizam automaticamente a quantidade no modelo [`geladinhos.models.Geladinho`](geladinhos/models.py) quando entradas/saídas são criadas.
- Ajuste `BASE_DIR`, `DATABASES` e variáveis de ambiente em [core/settings.py](core/settings.py) conforme seu ambiente (local / produção).

API: Api Integrada para consulta básica e Crud, além de futura Integracao.




