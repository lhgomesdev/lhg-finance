# 💰 LHG Finance

App web de controle financeiro pessoal, multiusuário (cada usuário com suas próprias finanças, separadas). Projeto pessoal e de portfólio.

Veja o planejamento completo em [`PROJETO.md`](PROJETO.md).

## Stack

- Django 6
- CSS puro (`static/css/main.css`, sem framework/build step)
- Chart.js (via CDN, só no dashboard)
- SQLite (dev local)

## Rodando localmente

```bash
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash) — use venv\Scripts\activate no cmd/PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000`.
