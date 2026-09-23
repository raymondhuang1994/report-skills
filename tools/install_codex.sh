#!/usr/bin/env bash
# 把仓库里的技能软链到 Codex 的技能目录（默认 ~/.agents/skills）。用法：tools/install_codex.sh [目标目录]
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; DEST="${1:-$HOME/.agents/skills}"; mkdir -p "$DEST"
for s in "$ROOT"/skills/*/; do n="$(basename "$s")"; ln -sfn "${s%/}" "$DEST/$n"; echo "linked $n -> $DEST/$n"; done
echo "完成。Codex 里输入 /skills 查看；用 \$exec-deep-report 这样的写法可显式调用。"
echo "首次使用先运行：python3 $ROOT/shared/scripts/doctor.py  以及  (cd $ROOT/shared/scripts && npm install)"
