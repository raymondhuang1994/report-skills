# 样例：「北极星」迷你报告（虚构）

这是文风与结构的锚点，不是内容来源。全部机构、产品、代码与数字都是虚构的，每份真实报告都必须从原始材料重新算。写作前读一遍，用来校准三件事：执行摘要怎么开场、攻防表两列怎么写、“惊人总结”怎么造出来并溯源。

- `polaris-mini.json`：可直接构建的迷你报告（摘要一页、四个短章、附录）。它同时是 `scripts/structure_qa.py` 的测试样本。
- `make_figures.py`：生成样例用到的一张图，顺带检验 `chart_style.py` 的中文字体是否可用。

构建看效果：

```bash
cd examples && python3 make_figures.py
node ../scripts/build.js polaris-mini.json /tmp/polaris.docx
python3 ../scripts/structure_qa.py polaris-mini.json --example
```

防抄用：`text_qa.py` 与 `structure_qa.py` 都把“北极星”列为样例标记词，真实报告里出现即报错。
