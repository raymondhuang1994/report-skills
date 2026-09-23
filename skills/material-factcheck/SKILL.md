---
name: material-factcheck
description: 用户要“核一下这份材料、数字对不对、口径一致吗、帮我复算、材料里有没有矛盾、路演 PPT 或单张能不能对外”时使用，面向基金、ETF 与金融产品的路演材料、单张、新闻稿、KFS。逐页提事实带页码，把图表底层数据抽出来与表格逐只加总核对，独立复算集中度与费用，列出口径矛盾、慎用词与需向产品团队确认的问题，交付核查备忘。要完整报告用 exec-deep-report；要话术用 sales-qa-battlecard。Also use to fact-check fund marketing decks and one-pagers in Chinese.
---

# 材料核查（material-factcheck）

## 什么时候用，什么时候不用

用：拿到一份路演材料、单张、新闻稿或 KFS，需要在对外或写报告之前确认数字能不能用、内部口径是否一致、哪些说法要改。也用于完整报告的阶段 1 到 2，此时产出直接进 `work/facts.md` 与 `work/recalc.md`。
不用：写完整报告（exec-deep-report）；写口号（product-slogan）；写话术（sales-qa-battlecard）。

## 原则

1. **图表要读底层数据，不读文字层。** 饼图、柱图的数值只在图表对象里，文字提取拿不到；用 `scripts/extract_pptx.py` 抽出来，再把图表页渲染成图片看一遍。
2. **每个宣称的数字都要有一个独立算出来的数字对照。** 材料说的地区分布、行业分布、前十大合计、费用总额，用成分股表逐只加总或用 `scripts/quant_tools.py` 复算；对得上写“一致”，对不上写差多少、差异可能来自什么口径。
3. **矛盾单列，不埋在段落里。** 每条矛盾写清：材料 A 说什么、材料 B 或加总说什么、差多少、本备忘以哪个为准、建议向谁确认。
4. **只核事实，不做判断。** 备忘不写“产品好不好”，只写“数字对不对、能不能这样说”。
5. **数字带页码与日期。** 材料里没写日期的数字，标“材料未注明日期”，列入待确认。

## 工作流

**步骤 1　抽取。** 运行 `python3 scripts/extract_pptx.py 材料.pptx out.json`，得到每页标题、文字、表格与图表数据；PDF 用文字提取加逐页渲染。把图表页渲染成图片逐页看，确认抽出的数字与图上标注一致。
**步骤 2　事实清单。** 按 `assets/memo-template.md` 第 1 节的表格逐条登记：编号、事实、页码、日期、级别（`references/evidence-discipline.md` 的 L1 至 L5）。承重事实（费用、集中度、地区或行业分布、指数规则、上市信息、结构与复制方式）必须齐。
**步骤 3　复算。** 至少做这几项：地区与行业分布按成分股逐只加总对饼图；前三大、前十大、HHI、有效持股数（`quant_tools.concentration`）；权重上限与实际最大权重；全成本（管理费、经常性开支估计与上限、是否含掉期费）；材料内两处出现的同一指标是否一致。算法与输入写进备忘第 2 节。
**步骤 4　矛盾与慎用词。** 差异超过四舍五入能解释的范围（单只权重四舍五入到 0.1% 时，n 只加总误差不超过 0.05n 个百分点）就算矛盾，列进第 3 节；对照 `references/caution-words.md` 扫一遍材料文字，命中的点名页码，列进第 4 节。
**步骤 5　待确认清单与交付。** 第 5 节列出需要向产品、指数公司或合规确认的问题，每条写谁能回答、影响哪个数字。备忘在对话内交付；也可写成 Markdown 文件。备忘顶部写材料名称、版本或日期、核查日期。

## 判定标准与常见矛盾类型

见 `references/checklist.md`：矛盾类型（图表与表格加总不一致、两页同一指标不一致、规则上限与实际权重不一致、估计值当实际值、回测当实盘、口径未注明）、每类的判定方法与写法。

## 与其他技能的关系

备忘是 product-slogan 与 sales-qa-battlecard 的事实来源；在 exec-deep-report 中，本技能对应阶段 1 与 2，产出写入 `work/facts.md` 与 `work/recalc.md`。四个技能可以单独用，也可以由 exec-deep-report 一次调用全部。

## 参考与脚本

| 文件 | 何时用 |
|---|---|
| `scripts/extract_pptx.py` | 步骤 1 抽取 PPT 文字、表格与图表数据 |
| `scripts/quant_tools.py` | 步骤 3 集中度、重叠度、费用覆盖等复算 |
| `references/checklist.md` | 步骤 3 到 5 的判定标准与矛盾类型 |
| `references/evidence-discipline.md` | 事实分级、转引与复核、数据缺口写法 |
| `references/caution-words.md` | 步骤 4 慎用词扫描 |
| `assets/memo-template.md` | 交付格式 |

版本 0.1（2026-09-22）。共用脚本与参考由团队共用目录同步，改动请改共用目录。
