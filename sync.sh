#!/usr/bin/env bash
set -e
msg="${1:-update}"
git pull --rebase
git add -A
if ! git diff --cached --quiet; then
  git commit -m "$msg"
fi
git push
