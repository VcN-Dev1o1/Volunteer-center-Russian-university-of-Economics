#!/bin/bash
set -euo pipefail

# Всегда работать из папки, где лежит скрипт
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

FILES=(
  "config/__init__.py"
  "config/asgi.py"
  "config/wsgi.py"
  "config/urls.py"
  "config/logging.py"
  "config/settings/__init__.py"
  "config/settings/base.py"
  "config/settings/dev.py"
  "config/settings/prod.py"

  "apps/__init__.py"
  "apps/accounts/__init__.py"
  "apps/accounts/admin.py"
  "apps/accounts/apps.py"
  "apps/accounts/forms.py"
  "apps/accounts/models.py"
  "apps/accounts/selectors.py"
  "apps/accounts/services.py"
  "apps/accounts/signals.py"
  "apps/accounts/permissions.py"
  "apps/accounts/urls.py"
  "apps/accounts/views.py"
  "apps/accounts/tests.py"
  "apps/accounts/migrations/__init__.py"
  "apps/accounts/templates/accounts/login.html"
  "apps/accounts/templates/accounts/profile_menu.html"
  "apps/accounts/templates/accounts/delete_request.html"
  "apps/accounts/templates/accounts/password_reset_telegram.html"

  "templates/base.html"
  "templates/partials/header.html"
  "templates/partials/lower_bar.html"
  "templates/partials/messages.html"
  "templates/errors/400.html"
  "templates/errors/401.html"
  "templates/errors/403.html"
  "templates/errors/404.html"
  "templates/errors/405.html"
  "templates/errors/413.html"
  "templates/errors/429.html"
  "templates/errors/500.html"

  "static/css/base.css"
  "static/js/menu.js"
  "media/.gitkeep"
)

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "Пропущено: $file"
    continue
  fi

  mkdir -p "$(dirname "$file")"
  if touch "$file"; then
    echo "Создано: $file"
  else
    echo "ОШИБКА: не удалось создать $file" >&2
    exit 1
  fi
done
