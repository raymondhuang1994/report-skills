# -*- coding: utf-8 -*-
"""text_qa.py —— 交付前的文字检查。用法：python3 text_qa.py 报告.docx [--extra 词1,词2]
检查：残留的 ** 标记；慎用词；过程性字眼；疑似罕见字；“转引”“待复核”“数据缺口”计数；未填的占位符。
慎用词命中不一定是错误（例如出现在慎用词表里），需要人工判断上下文。"""
import sys, re, subprocess

CAUTION = ["首只", "唯一", "独家", "全面覆盖", "稳赚", "保本", "零风险", "低风险", "更安全", "持久定价权", "必然", "保证收益", "最佳", "第一名"]
PROCESS = ["上一版", "v1 ", "V1 ", "另一个AI", "另一个 AI", "其他AI", "其他 AI", "用户提供", "如前所述我", "作为AI", "作为 AI"]
PLACEHOLDER = ["TODO", "待补", "XXX", "【】", "……。", "待校准"]
EXAMPLE_MARK = ["北极星", "样例机构", "样例指数公司", "样例交易所", "样例数据商"]  # examples/ 里的虚构样例标记，真实报告中出现即为抄用

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    extra = sys.argv[sys.argv.index("--extra") + 1].split(",") if "--extra" in sys.argv else []
    import shutil
    if not shutil.which("pandoc"): raise SystemExit("未找到 pandoc，无法提取文字；运行 scripts/doctor.py 查看安装方法")
    txt = subprocess.run(["pandoc", "-t", "plain", sys.argv[1]], capture_output=True, text=True).stdout
    lines = txt.splitlines(); print(f"字符数（含表格排版空白）：{len(txt)}；行数：{len(lines)}")
    def scan(title, words):
        hits = [(i + 1, w, l.strip()[:60]) for i, l in enumerate(lines) for w in words if w in l]
        print(f"\n[{title}] 命中 {len(hits)} 处"); [print(f"  行{n} 「{w}」 {ctx}") for n, w, ctx in hits[:25]]
    scan("残留标记", ["**"]); scan("慎用词", CAUTION + extra); scan("过程性字眼", PROCESS); scan("占位符", PLACEHOLDER); scan("样例标记词（应为0）", EXAMPLE_MARK)
    rare = sorted({c for c in txt if "\u3400" <= c <= "\u4dbf" or "\U00020000" <= c <= "\U0002ffff"})
    print(f"\n[疑似罕见字] {''.join(rare) or '无'}")
    for k in ["转引", "待复核", "数据缺口", "本报告测算", "建议值"]: print(f"[计数] {k}: {txt.count(k)}")
    nosrc = sum(1 for l in lines if re.match(r"\s*资料来源[:：]\s*$", l)); print(f"[空的资料来源行] {nosrc}")

if __name__ == "__main__": main()
