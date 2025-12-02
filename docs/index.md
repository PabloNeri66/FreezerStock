# Fauna - Gelados Management System

Sistema completo de gestão de estoque para produtos gelados, com entradas (inflows), saídas (outflows), dashboard com métricas e API REST.

---

## 🎯 Visão Geral
O **Fauna** é um sistema modular para gerenciamento de geladinhos:

- Cadastro de produtos com preço de custo e venda.
- Controle de quantidade em estoque.
- Registro de entradas (Inflow) e saídas (Outflow) de produtos.
- Atualização automática do estoque via signals.
- Dashboard com métricas detalhadas por produto e vendas gerais.
- Envio automático de relatórios por email.
- API REST para integração com frontends e sistemas externos.

---

## 📋 Checklist de Features

- [x] CRUD de Geladinhos  
- [x] CRUD de Entradas (Inflows)  
- [x] CRUD de Saídas (Outflows)  
- [x] Signals de atualização automática de estoque  
- [x] Dashboard com métricas  
- [x] API REST com Django REST Framework (DRF)  
- [x] Autenticação JWT  
- [x] Command de relatórios por email  
- [x] Paginação automática  
- [x] Docker support (`docker build -t fauna:latest .`)  
- [ ] Adicionar testes unitários para signals e commands  
- [ ] Documentação da API: Implementar Swagger/Redoc  
- [ ] Expandir relatórios com gráficos (Chart.js/Plotly)  
- [ ] Adicionar Redis para cache de métricas  
- [ ] Sistema de logging mais robusto  

---

## ✨ Funcionalidades

### Gestão de Produtos (Geladinhos)
- CRUD completo, histórico de criação/atualização.
- Controle de estoque e preços.
- Templates:
  - `geladinho_list.html`, `geladinho_create.html`, `geladinho_detail.html`, `geladinho_update.html`, `geladinho_delete.html`

### Gestão de Entradas (Inflows)
- Registro de novas entradas.
- Atualização automática do estoque via signal.
- Data de fabricação e descrição opcional.
- Templates: `inflow_list.html`, `inflow_create.html`, `inflow_detail.html`
- Signal: `update_geladinho_quantity()` — incrementa quantidade.

### Gestão de Saídas (Outflows)
- Registro de vendas e saídas.
- Atualização automática via signal.
- Templates: `outflow_list.html`, `outflow_create.html`, `outflow_detail.html`
- Signal: `update_geladinho_quantity()` — decrementa quantidade.
- Command: `smtp_sales_local.py` — envia relatórios por email.

### Dashboard e Métricas
- Componentes reutilizáveis em `core/templates/components/`:
  - `_geladinho_metrics.html`, `_sales_metrics.html`
  - `_header.html`, `_sidebar.html`, `_footer.html`, `pagination.html`
- Métricas em tempo real.
- Autenticação JWT.

---

## 🔧 Tecnologias
- Python 3.11 (Docker)  
- Django 5.2.7  
- Django REST Framework 3.16.1  
- PostgreSQL (via psycopg2-binary 2.9.11)  
- JWT Authentication (djangorestframework_simplejwt 5.5.1)  
- Gunicorn 23.0.0  
- Frontend com templates Jinja2 + componentes reutilizáveis  

---


## 🚀 Novidades / Commands

**`smtp_sales_local.py`**
- Localização: `outflows/management/commands/smtp_sales_local.py`
- Coleta vendas, formata relatório e envia email.
- Uso:
```bash
python manage.py smtp_sales_local
