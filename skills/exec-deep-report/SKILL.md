---
name: exec-deep-report
description: 用户要“做一份报告、深度分析、研究报告、战略建议、产品分析、竞品分析、汇报材料”，或提到“参考某份报告的水准”“给老板、CEO、董事会、产品委员会看”“融合另一份报告”“出高管版”“总结分析”时使用，即使没说要 Word、没说“深度”。这是为管理层、董事会、产品委员会或销售团队撰写中文深度研究报告的工作法与工具链，覆盖产品分析与营销方案、机构或行业深度分析、新品机会与候选池研究三类；含立项三问、两步交付、独立复算、证据分级、融合他稿与高管版规则、质量标尺，以及中文 Word 渲染库、图表样式与结构、文字、版式三道 QA 脚本。只想口号或定位用 product-slogan，只要问答与攻防表用 sales-qa-battlecard，只核对材料数字用 material-factcheck，只要排版用 cn-docx-report。Also use for executive research reports, board memos, product or competitive deep-dives written in Chinese.
---

# 高管深度报告工作法

## 这个技能解决什么

让团队里任何人都能稳定产出“有判断、有证据、可以直接交到管理层手里”的深度报告。它防的是两类失败：

- **内容失败**：有观点没证据，或有数据没判断；把宣传材料当事实；把预测写成已经发生的事。
- **流程失败**：没问清读者就开写；一次性交 40 页后被整体推翻；擅自删掉用户想保留的内容；Word 版式事故。

报告质量的上限来自材料与数据，本技能保证的是下限和一致性。

## 团队默认约定

下面是默认值，用户当次的明确指示优先。每条都写了原因，遇到没覆盖的情况按原因去判断。

1. **先方案、后执行。** 先给思路与方案，用户确认后再动手。深度报告的返工成本极高，十分钟的对齐能省掉几小时的重写。
2. **立项三问必须问清**：读者与口径（谁看、要多坦率）、交付形式、数据能否补充。三者任何一个不同，报告的写法都不同。已经在对话里说过的不要重复问。
3. **两步交付。** 第一步交“执行摘要 + 事实底稿 + 骨架 + 数据缺口”，确认后第二步才扩写完整 Word。判断错了，在第一步改只需要改一页。
4. **先独立、后融合。** 用户同时提供其他 AI 或同事的稿件时，先独立完成自己的版本，再按 `references/fusion-protocol.md` 融合。先读别人的结论会被带着走。
5. **不确定就问，不要猜。** 尤其是立场、取舍、内部事实（例如某产品的初始资金来源）。内部事实不知道就留空并标注，不要编。
6. **删改须逐项列出并经确认。** 想删除、合并或大幅改写已有内容时，先列清单，用户同意后再做。候选方案、备选项要完整保留，附上优先级和暂缓理由，最终取舍权在用户。
7. **证据纪律**：每个数字有来源和日期；估算标“测算”；拿不到就写“数据缺口”，不要用看似合理的数字填空。详见 `references/evidence-discipline.md`。
8. **标签克制。** 正文里只对三类内容加标签：推断、假设、建议。来源写在图表下方和附录，不要让正文布满括号。
9. **立场可以偏向委托方，但每条论据都要配一条“需要先承认的”。** 只讲好话的报告，管理层不会信，销售拿出去也会被客户问倒。
10. **默认交付**：简体中文、Word、结论式章节标题、图表优先；需要用户补的数据另出一份 Excel 取数单。

## 八个阶段

阶段 4 和阶段 7 之前各有一道闸门，必须停下来等用户确认。

### 阶段 0　立项
- 问清立项三问；判断报告类型，读 `references/skeletons.md` 里对应的骨架（A 产品分析与营销、B 机构或行业深度、C 新品机会与候选池）。
- 如果用户给了“参考某份报告的水准”，先把那份报告拆成写作公式（结构、论证方式、它为什么让人印象深刻），再决定沿用哪些。拆法见 `references/writing-formula.md`。范例只作水准参考，观点必须独立。
- **范围与输出确认。**立项三问之后，用选项确认这次要生成什么、调用到哪些模块、最终输出什么形式，默认全选即完整报告：材料核查与复算、外部坐标与同业、定位与口号、销售问答与攻防、营销与分发打法、目标情景与 KPI、Word 排版。用户去掉的模块不写，也不在报告里留空章。输出形式三选：Word 报告；Word 报告加独立工具文件（口号一页纸、核查备忘、问答攻防表、取数单）；只在对话内交付。
- 团队成员可以先填 `assets/brief-template.md` 再开始，能省掉一轮问答。
- 把 `assets/workspace/` 复制为报告目录下的 `work/`，之后每个阶段的产出写进对应文件（说明见 `assets/workspace/README.md`）。中断续写或换宿主时，新会话先读 `work/decisions.md`。
- 在 Claude 沙箱以外的环境（本机、Codex、CI）首次使用，先运行 `python3 scripts/doctor.py`，缺什么按提示安装。

### 阶段 1　吃透材料
- 全文提取用户给的每一份材料；**PPT 和 PDF 要把图表页渲染成图片看**，关键数字经常只存在于图里，文本提取不到。PPT 先跑 `python3 scripts/extract_pptx.py 材料.pptx out.json`，饼图与柱图的底层数值直接抽出来，阶段 2 用它对成分股表逐只加总。
- 列出两张清单：材料里的全部事实（带页码或出处），以及“材料里有、但没被提炼成结论”的素材。后者往往是报告亮点的来源。

### 阶段 2　独立复算
- 用材料自带的数据重新算一遍：逐项加总是否等于宣称的合计、同一日期的不同图表是否自洽、集中度与有效数量、与竞品的重叠度、费用的长期影响、对关键变量的敏感度。常用测算在 `scripts/quant_tools.py`。
- 这一步有两个产出：别人没算过、但可以完全溯源的新数字；以及材料内部的口径矛盾。口径矛盾要单独告诉用户，它通常比报告本身更急。

### 阶段 3　外部坐标
- 四类坐标：时点（报告发布时的市场环境）、标杆（正面、反面、自家各至少一个）、直接同业（费用、规模、结构、近况）、学术或监管依据。
- 一手文件优先：法律与监管文件、公司公告、交易所与指数公司官方资料，高于管理人网页，高于媒体，高于宣传材料。网页上的披露可能没有随文件更新。
- 涉及当前状态的事实（谁在任、产品是否已上市、费率、规模）一律检索核实，不凭印象写。

### 阶段 4　闸门一：交底稿
交付并停下等待确认：
- 执行摘要草稿：一个核心问题、三个左右核心判断、一句话定位或总论点；
- 事实底稿：关键数字表，逐条带来源与日期；
- 章节骨架：结论式标题；
- 数据缺口表与取数单草稿；
- 需要用户拍板的问题，用选项形式给出，附上自己的建议；
- 对照 `references/quality-rubric.md` 自评第 1 至 5 项，分数、证据位置与补救写进交付说明；低于 8 分（满分 10）先补再进入成稿。

### 阶段 5　成稿
- 按 `references/writing-formula.md` 写作；销售与决策工具的模板在 `references/toolkit-templates.md`。
- 动笔前读一遍 `examples/polaris-mini.json`，校准摘要开场、攻防表两列和“惊人总结”的写法。样例全部虚构，任何名称与数字都不得进入真报告。
- 正文写进 `work/report.json`（结构与样例相同），用 `node scripts/build.js work/report.json 报告.docx` 渲染；图表用 `scripts/chart_style.py` 生成 PNG。内容与版式分离后，同一份 JSON 重复构建结果一致，改文字不必碰脚本。`scripts/build_template.js` 仍可作为直接调用渲染库的参考。
- 宿主提供 docx 技能时（Claude 环境）同时读取；其他宿主直接用 `scripts/` 里的库。
- 执行摘要控制在两页内，读完摘要就能复述核心判断。

### 阶段 6　红队与核验
- 自查：每个数字能否指到来源；结论是否被证据支撑；有没有把预测写成事实、把备案写成上市、把指引写成实际；立场偏向处是否配了“需要承认的”。
- 融合其他稿件时执行 `references/fusion-protocol.md`：抽查对方至少三项承重数据，核实不了的标“转引，待复核”。
- 先跑 `python3 scripts/structure_qa.py work/report.json`，零 FAIL 再构建（它检查来源行、章内图表、问答条数、适配矩阵、攻防表、建议值标注、重要提示、占位符与样例标记）。
- 再跑 `scripts/render_qa.py` 与 `scripts/text_qa.py`，**逐页看渲染图**；把 render_qa 生成的 PDF 传给 `structure_qa.py --pdf` 可实测执行摘要页数。版式常见坑见 `references/docx-pitfalls.md`。

### 阶段 7　闸门二：交付包
- 报告本体，加一段交付说明：做了什么、改了什么、没做什么、哪些未核实、需要用户补什么、十项标尺自评（低于 17 分或任一项 0 分不交付）、技能版本与所用模型。模板见 `references/delivery-pack.md`。
- 需要用户从 Wind、彭博或内部系统补的数据，生成 Excel 取数单：宿主有 xlsx 技能用它，否则用 `scripts/make_datasheet.py`；列定义见 `references/evidence-discipline.md`。
- 用户要向上汇报时，给可直接粘贴的汇报话术。
- 用户要“高管版”时，按 `references/exec-version-rules.md` 改写，删改清单先行。

## 工具链

| 文件 | 用途 |
|---|---|
| `scripts/report_lib.js` | Word 渲染库：封面、手工目录、结论式标题、表格、提示框、图片、列表、页眉页脚。已处理行距、表格跨页、页码字号等问题 |
| `scripts/build.js` | 从 `report.json` 构建 Word，内容与渲染分离；`node build.js report.json out.docx` |
| `scripts/structure_qa.py` | 结构检查：十条硬规则变成 FAIL/WARN；可传 PDF 实测执行摘要页数 |
| `scripts/doctor.py` | 环境预检：node、docx、Python 库、LibreOffice、poppler、pandoc、中文字体，缺什么给安装命令 |
| `scripts/make_datasheet.py` | Excel 取数单兜底（openpyxl），宿主没有 xlsx 技能时用 |
| `scripts/extract_pptx.py` | 抽取 PPT 每页文字、表格与图表底层数据（饼图数值只在图表对象里），阶段 1 核对口径用 |
| `scripts/build_template.js` | 直接调用渲染库的最小示例，供改库或排查时参考 |
| `scripts/chart_style.py` | 统一的中文图表样式与常用图形（横向条形、高亮柱状、权重加累计、时段图、折线对比） |
| `scripts/quant_tools.py` | 集中度与有效数量、分组加总、组合重叠度、费用拖累、权重敏感度、交易时段重合、整手成本 |
| `scripts/render_qa.py` | Word 转 PDF 再转缩略图总览，报告页数，支持放大指定页 |
| `scripts/text_qa.py` | 文字检查：残留标记、慎用词、罕见字、对旧版本的指涉、“转引”计数 |

运行方式：在 `scripts/` 下执行一次 `npm install`（按 `package.json` 锁定 docx 版本），之后 `node scripts/build.js ...` 直接可用；已全局安装 docx 的环境也可用 `NODE_PATH=$(npm root -g)`。Python 脚本直接运行。依赖 matplotlib、Pillow、openpyxl、LibreOffice、poppler、pandoc；Claude 的代码执行环境里都已具备，其他环境先跑 `doctor.py`。

## 参考文件索引

| 文件 | 什么时候读 |
|---|---|
| `references/skeletons.md` | 阶段 0，选定报告类型时 |
| `references/writing-formula.md` | 阶段 0 拆解范例、阶段 5 写作时 |
| `references/evidence-discipline.md` | 阶段 1 至 3 采集数据、阶段 7 出取数单时 |
| `references/toolkit-templates.md` | 需要问答口径、攻防表、适配矩阵、慎用词表、情景目标、KPI、行动清单、风险矩阵、决策选项表、候选池评分表时 |
| `references/fusion-protocol.md` | 用户提供其他 AI 或同事的稿件要求融合时 |
| `references/exec-version-rules.md` | 用户要高管版、汇报版、精简版时 |
| `references/delivery-pack.md` | 阶段 4 与阶段 7 交付时 |
| `references/docx-pitfalls.md` | 生成 Word 之前，以及版式出问题时 |
| `references/quality-rubric.md` | 闸门一与闸门二自评时；维护人复评与回放时 |
| `references/caution-words.md` | 写话术、口号、问答前；阶段 6 文字检查时 |
| `examples/polaris-mini.json` | 阶段 5 动笔前校准文风；全部虚构，不得引用 |
| `assets/workspace/` | 阶段 0 复制为 `work/`；中断续写时先读 |

## 最常见的五个失败

1. **没等确认就写完整版。** 两步交付是为了让错误便宜，不要跳过闸门一。
2. **把宣传材料当事实来源。** 路演材料和新闻稿可以引用，但要与逐项加总和官方文件交叉核对。
3. **用回测或历史涨幅当卖点。** 实盘与回测分开讲，盈利与估值分开讲。
4. **小故事盖过大权重。** 讲占比很小的亮点案例时必须同时标出它的占比，决定结果的是大权重部分。
5. **不看渲染图就交付。** 图片被压扁、表格孤行、目录空白，只有逐页看才能发现。

## 版本与维护

当前版本 1.2（2026-09-22），变更见 `CHANGELOG.md`。本技能是编排器：四个卫星技能（product-slogan、material-factcheck、sales-qa-battlecard、cn-docx-report）各自可单独使用，本技能一次覆盖全部；共用的参考与脚本由团队共用目录同步。每份报告交付后，把新踩的坑写进 `references/docx-pitfalls.md`，把新用到的表格写进 `references/toolkit-templates.md`，把用户反复重申的新约定写进本文件的“团队默认约定”，把 `structure_qa.py` 抓不到的新规则加进去，然后升版本号、回放金标准（得分不低于上一版）再分发。修改默认约定前先与团队确认，因为它会改变所有人的产出。
