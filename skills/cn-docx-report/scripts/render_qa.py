# -*- coding: utf-8 -*-
"""render_qa.py —— Word 转 PDF 再转缩略图总览，用于逐页检查版式。
用法：python3 render_qa.py 报告.docx [输出目录] [--zoom 9,16,21]
输出：页数、总览图 sheet_N.png（每张 8 页）、可选的放大页 zoom_N.png。生成后必须用看图工具逐张查看。"""
import sys, os, glob, subprocess, shutil

def to_pdf(docx, outdir):
    wrapper = "/mnt/skills/public/docx/scripts/office/soffice.py"  # Claude 环境里的封装脚本；没有就直接调用 soffice（含 Mac 安装路径）
    soffice = next((c for c in ["soffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice", "/usr/local/bin/soffice"] if shutil.which(c) or os.path.exists(c)), None)
    if not os.path.exists(wrapper) and not soffice: raise SystemExit("未找到 LibreOffice，无法转 PDF；运行 scripts/doctor.py 查看安装方法")
    cmd = (["python3", wrapper] if os.path.exists(wrapper) else [soffice]) + ["--headless", "--convert-to", "pdf", "--outdir", outdir, docx]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(docx))[0] + ".pdf")
    if not os.path.exists(pdf): raise SystemExit("转换 PDF 失败：请确认 LibreOffice 可用")
    return pdf

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    docx = os.path.abspath(sys.argv[1]); args = [a for a in sys.argv[2:] if not a.startswith("--")]
    outdir = os.path.abspath(args[0]) if args else os.path.join(os.path.dirname(docx), "render_qa")
    zoom = []
    if "--zoom" in sys.argv: zoom = [int(x) for x in sys.argv[sys.argv.index("--zoom") + 1].split(",")]
    shutil.rmtree(outdir, ignore_errors=True); os.makedirs(outdir)
    work = os.path.join(outdir, "in.docx"); shutil.copy(docx, work)
    pdf = to_pdf(work, outdir)
    subprocess.run(["pdftoppm", "-r", "55", "-png", pdf, os.path.join(outdir, "p")], check=True)
    from PIL import Image
    pages = sorted(glob.glob(os.path.join(outdir, "p-*.png"))); print("pages:", len(pages))
    for k in range(0, len(pages), 8):
        ims = [Image.open(f) for f in pages[k:k + 8]]; w, h = ims[0].size; rows = (len(ims) + 3) // 4
        sheet = Image.new("RGB", (w * 4, h * rows), "white")
        for i, im in enumerate(ims): sheet.paste(im, ((i % 4) * w, (i // 4) * h))
        name = os.path.join(outdir, f"sheet_{k // 8 + 1}.png"); sheet.save(name); print("sheet:", name, f"(第 {k + 1}–{k + len(ims)} 页)")
    for n in zoom:
        subprocess.run(["pdftoppm", "-r", "85", "-f", str(n), "-l", str(n), "-png", pdf, os.path.join(outdir, "zoom")], check=True)
    for f in sorted(glob.glob(os.path.join(outdir, "zoom-*.png"))): print("zoom:", f)

if __name__ == "__main__": main()
