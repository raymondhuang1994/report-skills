#!/usr/bin/env bash
# 安装各入口依赖，再安全软链到 Codex。用法：tools/install_codex.sh [目标目录]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$HOME/.agents/skills}"
if [ "$#" -gt 1 ]; then echo "用法：tools/install_codex.sh [目标目录]" >&2; exit 2; fi
for tool in node npm python3; do
  if ! command -v "$tool" >/dev/null; then echo "缺少 ${tool}，请先安装；尚未创建技能链接。" >&2; exit 1; fi
done

check_target() {
  local source="$1" target="$2"
  if [ -L "$target" ]; then
    if ! [ "$target" -ef "$source" ]; then
      echo "拒绝替换已有链接：${target}；请先检查并选择新的安装目录。" >&2; return 1
    fi
  elif [ -e "$target" ]; then
    echo "拒绝覆盖已有文件或目录：${target}；请先检查并选择新的安装目录。" >&2; return 1
  fi
}

# 先检查所有目标，避免安装半套后才遇到同名文件。
for skill in "$ROOT"/skills/*/; do
  check_target "${skill%/}" "$DEST/$(basename "$skill")"
done
for scripts in "$ROOT/shared/scripts" "$ROOT"/skills/*/scripts; do
  if [ -f "$scripts/package.json" ]; then
    echo "安装依赖：$scripts"
    npm install --prefix "$scripts" --ignore-scripts --no-audit --no-fund --package-lock=false
  fi
done
echo "检查系统依赖；缺失项需按 doctor 提示安装，不会自动修改系统。"
python3 "$ROOT/shared/scripts/doctor.py"
# 依赖确实可从每个实际技能入口解析，不借助全局 NODE_PATH。
for scripts in "$ROOT"/skills/*/scripts; do
  if [ -f "$scripts/package.json" ]; then
    (cd "$scripts" && env -u NODE_PATH node -e 'require("docx"); console.log("技能依赖 OK：" + process.cwd())')
  fi
done
mkdir -p "$DEST"
for skill in "$ROOT"/skills/*/; do
  target="$DEST/$(basename "$skill")"
  check_target "${skill%/}" "$target"
  if [ -L "$target" ]; then echo "已安装：$target"; else ln -s "${skill%/}" "$target"; echo "linked $target"; fi
done
echo "完成。Codex 里输入 /skills 查看；用 \$exec-deep-report 可显式调用。系统依赖已检查，版式交付仍须逐页目视检查。"
