# Codex 实测清单

在本机按顺序做，每项记录结果与日期。

| # | 检查 | 命令或操作 | 通过标准 |
|---|---|---|---|
| 1 | 预检 | `python3 shared/scripts/doctor.py` | 必需项全 OK；中文字体找到 PingFang 或 Noto |
| 2 | 依赖 | `cd shared/scripts && npm install && cd - && tools/selftest.sh` | 自检七步通过（本机有 LibreOffice 时第 7 步也通过） |
| 3 | 安装 | `tools/install_codex.sh`，Codex 里 `/skills` | 五个技能出现在列表，描述前半段可读 |
| 4 | 触发 | 给 Codex 一份公开路演 PPT，说“帮我核一下这份材料的数字” | 触发 `material-factcheck`，运行 extract_pptx.py，饼图数值与逐只加总同时出现 |
| 5 | 闸门 | 说“做一份产品分析与营销报告，先给思路” | 触发 `exec-deep-report`，用选项确认范围与输出，停在闸门一 |
| 6 | 联网 | 观察第 5 项里外部坐标一节 | 能检索：数字带检索日期；不能检索：写入数据缺口，不用记忆数字 |
| 7 | 看图 | 让它跑 `render_qa.py` 并评价版式 | 能看图：指出具体页的问题；不能看图：明确说明“未目视检查” |
| 8 | 回放 | 用私有金标准的回放提示词与两份原始材料 | 闸门一评分不低于 Claude 侧基线；M1、M2 复现 |

记录位置：`evals/replay-log.md`（私有，不提交）。
