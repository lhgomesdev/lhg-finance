# 💰 LHG Finance

[![CI](https://github.com/lhgomesdev/lhg-finance/actions/workflows/ci.yml/badge.svg)](https://github.com/lhgomesdev/lhg-finance/actions/workflows/ci.yml)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

App web de controle financeiro pessoal, multiusuário — cada usuário gerencia suas próprias finanças, separadas dos demais. Projeto pessoal e de portfólio.

**🔗 No ar:** [finance.lhgomes.dev.br](https://finance.lhgomes.dev.br)

## ✨ Funcionalidades

- **Transações:** cadastro, edição e exclusão de receitas e despesas, com data, descrição, valor e observações.
- **Categorias:** categorias próprias por usuário, separadas por tipo (receita/despesa) e com cor de identificação; todo usuário novo já recebe um conjunto padrão.
- **Dashboard:** resumo do mês (receita/despesa/saldo) e gráfico de gastos por categoria (Chart.js).
- **Listagem com filtro por mês:** navegação entre meses, com resumo do período.
- **Multiusuário:** autenticação própria (Django `auth`) — cada conta enxerga só os seus dados.
- **Dark mode:** segue o tema do sistema por padrão, com alternância manual salva por dispositivo.

## 🛠️ Stack

- Django 6
- CSS puro (`static/css/main.css`, sem framework/build step)
- Chart.js (via CDN, só no dashboard)
- SQLite (dev local) / PostgreSQL via [Supabase](https://supabase.com) (produção)
- Deploy: [Render](https://render.com), com WhiteNoise servindo os estáticos, atrás de domínio próprio via Cloudflare

## 📂 Estrutura do projeto

```
lhg-finance/
├── accounts/        # autenticação, cadastro, comando ensure_superuser
├── finance/          # transações, categorias, dashboard e CRUD
├── config/           # settings e urls do projeto Django
├── templates/         # templates HTML (base + por app)
├── static/            # CSS puro
├── build.sh            # build de produção (Render): deps, collectstatic, migrate, superuser
├── render.yaml           # Blueprint do Render
├── manage.py
└── requirements.txt
```

## 🚀 Rodando localmente

```bash
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash) — use venv\Scripts\activate no cmd/PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000`. Sem `.env`, roda com SQLite e `DEBUG=True` por padrão (veja `.env.example` pra customizar).

## ☁️ Deploy (Render + Supabase)

1. **Banco (Supabase):** crie um projeto em [supabase.com](https://supabase.com) e copie a connection string em *Project Settings → Database → Connection string → URI*.
2. **Web service (Render):** conecte este repositório em [render.com](https://render.com) — o `render.yaml` já configura build (`build.sh`: instala dependências, roda `collectstatic`, `migrate` e `ensure_superuser`) e start (`gunicorn config.wsgi:application`).
3. Defina `DATABASE_URL` no painel do Render com a connection string do Supabase (`SECRET_KEY` já é gerada automaticamente pelo Blueprint).
4. **Superusuário sem Shell** (indisponível no plano free): defina `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` e `DJANGO_SUPERUSER_PASSWORD` como variáveis de ambiente — o `build.sh` cria o superusuário automaticamente (uma única vez; é seguro deixar rodando em todo deploy). Depois de confirmar que funcionou, remova `DJANGO_SUPERUSER_PASSWORD` do painel por segurança.
5. **Domínio próprio:** em *Settings → Custom Domains* no Render, adicione o domínio e aponte um `CNAME` pra ele no seu provedor de DNS (`DNS only`, sem proxy, até o certificado SSL ser emitido). Adicione o domínio em `ALLOWED_HOSTS` e `https://` + domínio em `CSRF_TRUSTED_ORIGINS` nas variáveis de ambiente.
