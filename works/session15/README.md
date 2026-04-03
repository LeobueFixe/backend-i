# session15: Django setup + models

This session introduces relational persistence using Django ORM.

## Setup

1. Activate venv (if needed):
   - `source /workspaces/backend-i/.venv/bin/activate`
2. Install dependency:
   - `pip install django`
3. Create project:
   - `cd /workspaces/backend-i/works/session15`
   - `django-admin startproject backend_i_django .` (or `python -m django startproject backend_i_django .`)
4. Create app:
   - `python manage.py startapp meetings`
5. Add `'meetings'` to `INSTALLED_APPS` in `backend_i_django/settings.py`

## Models

`works/session15/meetings/models.py`:
- Meeting
- ActionItem (ForeignKey to Meeting, on_delete=models.CASCADE)

## Migrations

`python manage.py makemigrations`
`python manage.py migrate`

## Verify

`python manage.py shell`
```python
from meetings.models import Meeting, ActionItem
m = Meeting.objects.create(title='Planning', date='2026-03-10', owner='Jorge')
ActionItem.objects.create(meeting=m, description='Task 1', owner='Jorge', due_date='2026-03-20')
print(Meeting.objects.count(), ActionItem.objects.count(), m.action_items.count())
```

## Goal

- Provide Django ORM persistence with one-to-many Meeting -> ActionItem + cascade delete integrity.
