#!/usr/bin/env bash
# 自检：共享同步、frontmatter、渲染可重复、结构检查能抓缺陷。用法：tools/selftest.sh（CI 与本机通用；没有 LibreOffice 时跳过版式渲染）
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; S="$ROOT/shared"; T="$(mktemp -d)"
export NODE_PATH="${NODE_PATH:-$(npm root -g 2>/dev/null || true)}"
echo "[1] 共享同步与 frontmatter";  python3 "$ROOT/tools/package_skills.py" --check
echo "[2] 环境预检";                 python3 "$S/scripts/doctor.py" || echo "    （有缺失项，以下步骤可能跳过）"
echo "[3] 样例图";                   (cd "$S/examples" && python3 make_figures.py >/dev/null)
echo "[4] 构建两次并比较 word/*.xml"
node "$S/scripts/build.js" "$S/examples/polaris-mini.json" "$T/a.docx" >/dev/null && node "$S/scripts/build.js" "$S/examples/polaris-mini.json" "$T/b.docx" >/dev/null
mkdir -p "$T/a" "$T/b" && unzip -qo "$T/a.docx" -d "$T/a" && unzip -qo "$T/b.docx" -d "$T/b" && diff -rq "$T/a/word" "$T/b/word" && echo "    一致"
echo "[5] 结构检查：样例应 0 FAIL";   python3 "$S/scripts/structure_qa.py" "$S/examples/polaris-mini.json" --example | tail -1
echo "[6] 结构检查：植入缺陷应报 FAIL"
python3 - "$S/examples/polaris-mini.json" "$T/bad.json" <<'PY'
import json,sys; s=json.load(open(sys.argv[1],encoding='utf-8')); c=s['content']
qa=next(x for x in c if x[0]=='t' and any('怎么问' in h for h in x[1]['head'])); qa[1]['rows']=qa[1]['rows'][:8]
fig=next(x for x in c if x[0]=='f'); fig[1]['src']=''
json.dump(s,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False)
PY
if python3 "$S/scripts/structure_qa.py" "$T/bad.json" --example >/dev/null; then echo "    错误：植入缺陷未被发现"; exit 1; else echo "    已发现（预期）"; fi
if command -v soffice >/dev/null || [ -x /Applications/LibreOffice.app/Contents/MacOS/soffice ]; then
  echo "[7] 版式渲染";  python3 "$S/scripts/render_qa.py" "$T/a.docx" "$T/render" | tail -2
  out="$(python3 "$S/scripts/structure_qa.py" "$S/examples/polaris-mini.json" --example --pdf "$T/render/in.pdf")"; echo "$out" | grep "执行摘要"
else echo "[7] 版式渲染：无 LibreOffice，跳过"; fi
echo "自检完成"
