# -*- coding: utf-8 -*-
"""structure_qa.py —— 对 report.json 做结构检查，把技能里的硬规则变成可执行的检查。
用法：python3 structure_qa.py report.json [--pdf 报告.pdf] [--example]
  --pdf      传入 render_qa 生成的 PDF，可实测执行摘要页数
  --example  允许样例标记词（只在检查 examples/ 时使用）
退出码：有 FAIL 为 1，否则 0。WARN 需要人工判断，不影响退出码。
检查的规则（编号与输出对应）：
  F1 封面口径声明与目录存在            F6 适配矩阵至少两行“不适合/优势不充分/匹配度有限”
  F2 每张图有来源（src）               F7 攻防表“需要先承认的”一列无空格
  F3 含外部数据的表后两项内有资料来源行（自编工具表降为 WARN）   F8 情景目标表附近标注“建议值”
  F4 每个 h1 章至少一张表或图（附录/结语降为 WARN）   F9 存在“重要提示”提示框
  F5 质疑问答表不少于 10 行            F10 无占位符、样例标记词、过程性字眼
  W1 h1 标题过短，可能不是结论句       W2 执行摘要疑似超过两页（无 PDF 时按字数估）
"""
import sys, re, json, subprocess, shutil

PLACEHOLDER = ["TODO", "待补", "XXX", "【】", "……。", "〔示例", "待校准"]
EXAMPLE_MARK = ["北极星", "样例机构", "样例指数公司", "样例交易所", "样例数据商"]
PROCESS = ["上一版", "另一个AI", "另一个 AI", "其他AI", "其他 AI", "用户提供", "作为AI", "作为 AI"]

def strings(x):  # 递归取出所有字符串
    if isinstance(x, str): return [x]
    if isinstance(x, dict): return [s for v in x.values() for s in strings(v)]
    if isinstance(x, list): return [s for v in x for s in strings(v)]
    return []

def table_is(head, *pats):
    h = "｜".join(str(c) for c in head)
    return all(re.search(p, h) for p in pats)

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    args = sys.argv[1:]; allow_example = "--example" in args
    pdf = args[args.index("--pdf") + 1] if "--pdf" in args else None
    spec = json.load(open(args[0], encoding="utf-8")); content = spec.get("content", []); doc = spec.get("doc", {})
    fails, warns = [], []
    F = lambda code, msg: fails.append(f"FAIL {code} {msg}"); W = lambda code, msg: warns.append(f"WARN {code} {msg}")

    # F1
    if not (doc.get("cover") or {}).get("disclaimer"): F("F1", "封面缺少口径声明 disclaimer")
    if not spec.get("toc"): F("F1", "缺少目录 toc")

    # 按 h1 分章
    chapters, cur = [], None
    for idx, item in enumerate(content):
        if item[0] == "h1": cur = {"title": item[1], "items": [], "idx": idx}; chapters.append(cur)
        elif cur is not None: cur["items"].append(item)

    for i, item in enumerate(content):
        kind = item[0]; v = item[1] if len(item) > 1 else None
        nxt = [x[0] for x in content[i + 1:i + 3]]
        if kind == "f" and not (isinstance(v, dict) and str(v.get("src", "")).strip()): F("F2", f"第{i}项 图「{(v or {}).get('cap', '')[:30]}」缺少来源 src")
        if kind == "t":
            head = v.get("head", []); rows = v.get("rows", [])
            if "s" not in nxt:
                body = " ".join(strings(rows)); external = bool(re.search(r"\d[\d,.]*\s*(%|％|亿|万|bp|港元|美元|人民币|日元|韩元|新台币)|20[1-3]\d年|20[1-3]\d[/-]\d", body))
                tool = table_is(head, r"情景|KPI|阶段|动作|验收|风险|概率|表述|替代|候选|层次|客群|方向|需要的数据|观察对象|周次")
                (W if (tool or not external) else F)("F3", f"第{i}项 表「{'｜'.join(map(str, head))[:30]}」后两项内没有资料来源行 s" + ("（自编工具表，建议写“资料来源：本报告整理”）" if tool or not external else ""))
            if table_is(head, r"怎么问|质疑|问题", r"答") and len(rows) < 10: F("F5", f"第{i}项 质疑问答表只有 {len(rows)} 行，要求不少于 10 行")
            if table_is(head, r"适配判断"):
                n = sum(1 for r in rows if any(re.search(r"不适合|优势不充分|匹配度有限", str(c)) for c in r))
                if n < 2: F("F6", f"第{i}项 适配矩阵只有 {n} 行“不适合/优势不充分/匹配度有限”，要求至少 2 行")
            if table_is(head, r"需要先承认"):
                col = [j for j, c in enumerate(head) if re.search(r"需要先承认", str(c))][0]
                empty = [r[0] for r in rows if len(r) <= col or not str(r[col]).strip() or str(r[col]).strip() in ("—", "-", "无")]
                if empty: F("F7", f"第{i}项 攻防表以下维度“需要先承认的”为空：{empty}")
            if table_is(head, r"情景") and table_is(head, r"目标|规模"):
                near = " ".join(strings(content[i + 1:i + 3])); before = " ".join(strings(content[max(0, i - 2):i]))
                if "建议值" not in near + before: F("F8", f"第{i}项 情景目标表附近没有“建议值”标注")

    # F4
    for ch in chapters:
        if not any(x[0] in ("t", "f") for x in ch["items"]):
            (W if re.search(r"附录|结语", ch["title"]) else F)("F4", f"章「{ch['title'][:30]}」没有表或图")
        title = re.sub(r"^第[一二三四五六七八九十\d]+章[\s　]*", "", ch["title"]).strip()
        if title != "执行摘要" and len(title) < 8: W("W1", f"h1「{ch['title']}」只有 {len(title)} 字，可能不是结论句")

    # F9
    if not any(x[0] == "c" and "重要提示" in str(x[1].get("title", "")) for x in content): F("F9", "缺少“重要提示”提示框")

    # F10
    alltext = strings(content) + strings(doc)
    for w in PLACEHOLDER + PROCESS + ([] if allow_example else EXAMPLE_MARK):
        hits = [s[:40] for s in alltext if w in s]
        if hits: F("F10", f"出现「{w}」{len(hits)} 处，例如：{hits[0]}")

    # W2 执行摘要页数
    summ = next((c for c in chapters if "执行摘要" in c["title"]), None)
    if summ:
        if pdf and shutil.which("pdftotext"):
            norm = lambda t: re.sub(r"\s|\u3000", "", t)
            info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout if shutil.which("pdfinfo") else ""
            m = re.search(r"Pages:\s+(\d+)", info); total = int(m.group(1)) if m else 300
            def page_of(text, start=3):  # 从第 3 页起找，跳过封面与目录页
                for n in range(start, total + 1):
                    out = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), pdf, "-"], capture_output=True, text=True).stdout
                    if norm(text) in norm(out): return n
                return None
            s0 = page_of(summ["title"][:6]); k = chapters.index(summ)
            nxt_title = re.sub(r"^第[一二三四五六七八九十\d]+章[\s　]*", "", chapters[k + 1]["title"]) if k + 1 < len(chapters) else ""  # 去掉“第N章”，页眉文字可能插在中间
            s1 = page_of(nxt_title[:8]) if nxt_title else None
            if s0 and s1:
                pages = s1 - s0
                print(f"[执行摘要] 起于第 {s0} 页，下一章起于第 {s1} 页，占 {pages} 页")
                if pages > 2: F("W2", f"执行摘要占 {pages} 页，要求不超过 2 页")
            else: W("W2", "无法在 PDF 中定位执行摘要或下一章标题，页数未实测")
        else:
            chars = sum(len(s) for s in strings([x for x in summ["items"] if x[0] in ("p", "n", "b", "c")]))
            tables = sum(1 for x in summ["items"] if x[0] in ("t", "f"))
            if chars > 1800 or tables > 3: W("W2", f"执行摘要正文约 {chars} 字、{tables} 张表图，可能超过两页；以 render_qa 为准")

    n_t = sum(1 for x in content if x[0] == "t"); n_f = sum(1 for x in content if x[0] == "f")
    print(f"章数 {len(chapters)}；表 {n_t}；图 {n_f}；来源行 {sum(1 for x in content if x[0] == 's')}")
    for m in fails + warns: print(m)
    print(f"结果：{len(fails)} FAIL，{len(warns)} WARN")
    sys.exit(1 if fails else 0)

if __name__ == "__main__": main()
