#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-main}"
MSG="${1:-update}"

# 1) Проверка, что мы в git-репозитории
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "Not a git repository"
  exit 1
}

# 2) Переключиться на main (если вы случайно в другой ветке)
current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" != "$BRANCH" ]]; then
  git checkout "$BRANCH"
fi

# 3) Убедиться, что upstream настроен (иначе pull без указания ветки ломается)
if ! git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
  git branch --set-upstream-to="$REMOTE/$BRANCH" "$BRANCH"
fi

# 4) Подтянуть изменения с rebase
git pull --rebase "$REMOTE" "$BRANCH"

# 5) Добавить изменения
git add -A

# 6) Если изменений нет — просто выйти
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

# 7) Коммит и пуш
git commit -m "$MSG"
git push "$REMOTE" "$BRANCH"

echo "Done: pushed to $REMOTE/$BRANCH"
