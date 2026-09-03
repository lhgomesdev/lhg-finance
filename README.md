# 💰 LHG Finance

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white)

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
- SQLite (dev local)

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

Acesse `http://127.0.0.1:8000`.
