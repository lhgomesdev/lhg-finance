# 💰 LHG Finance

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

App web de controle financeiro pessoal, multiusuário — cada usuário gerencia suas próprias finanças, separadas dos demais. Projeto pessoal e de portfólio.

## ✨ Funcionalidades

- **Transações:** cadastro, edição e exclusão de receitas e despesas, com data, descrição, valor e observações.
- **Categorias:** categorias próprias por usuário, separadas por tipo (receita/despesa) e com cor de identificação.
- **Dashboard:** visão geral das finanças com gráficos interativos (Chart.js).
- **Multiusuário:** autenticação própria (Django `auth`) — cada conta enxerga só os seus dados.

## 🛠️ Stack

- Django 6
- CSS puro (`static/css/main.css`, sem framework/build step)
- Chart.js (via CDN, só no dashboard)
- SQLite (dev local) / PostgreSQL via [Supabase](https://supabase.com) (produção)
- Deploy: [Render](https://render.com), com WhiteNoise servindo os estáticos

## 📂 Estrutura do projeto

```
lhg-finance/
├── accounts/        # autenticação e contas de usuário
├── finance/          # transações, categorias e dashboard
├── config/           # settings e urls do projeto Django
├── templates/         # templates HTML (base + por app)
├── static/            # CSS puro
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
2. **Web service (Render):** conecte este repositório em [render.com](https://render.com) — o `render.yaml` já configura build (`build.sh`: instala dependências, roda `collectstatic` e `migrate`) e start (`gunicorn config.wsgi:application`).
3. Defina a variável de ambiente `DATABASE_URL` no painel do Render com a connection string do Supabase (`SECRET_KEY` já é gerada automaticamente pelo Blueprint).
4. Depois do primeiro deploy, crie um superusuário via Shell do Render: `python manage.py createsuperuser`.
