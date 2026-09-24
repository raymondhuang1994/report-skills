# report-skills：有证据、有记忆点的中文研究与营销材料

版本 **1.3.0**。先帮使用者选范围与叙事，确认后再研究成稿。
保留深度报告能力，也支持只做几块营销材料或优化现稿。

## 怎么开始

在 Codex 对话里输入：

> 用 $exec-deep-report 根据附件推荐方案。先让我选完整分析、部分模块或优化现稿，
> 给几个不同的叙事方向和小样，说明推荐理由；我确认后再执行。
> 我喜欢的原句请保留，不要悄悄改掉。

也可以直接说：“只做三条费用问答”“已有报告，只改定位和开场”。
已给出的范围和确认不会重问；没有确认就不自动写长稿。

## 五个技能

| 技能 | 用途 |
|---|---|
| exec-deep-report | 研究与营销编排：完整分析、选做模块、优化现稿；方向确认、主张卡、按需交付 |
| product-slogan | 先选不同叙事，再精修候选；研究/传播/双层表达，原句保留，多语言按需 |
| sales-qa-battlecard | 口语问答、攻防、客户适配；完整销售包或指定几题 |
| material-factcheck | 核查数字、日期、口径与计算，不把材料宣传直接当事实 |
| cn-docx-report | 按所选篇幅构建 Word，结构/文字/版式检查 |

创意选项先少后多：通常先三个方向各一个代表句，选中后再展开。
原句可逐字保留（exact）、保留气质（spirit）、仅作参考（reference）；
证据不足时保留为候选并给解释，不把喜好当事实背书。
完整已生成候选保留，但未支持的表述不会进入对外推荐。

## Codex 安装

需要 git、Node.js 18+、npm、Python 3。
以下脚本只安装仓库内 Node 依赖和用户级技能链接，不自动安装系统软件。

```bash
git clone https://github.com/raymondhuang1994/report-skills.git
cd report-skills
bash tools/install_codex.sh
```

脚本会为 shared 及每个实际渲染技能安装本地 docx 依赖，再检查 Python、LibreOffice、
Poppler、Pandoc、中文字体；缺项会停止并列提示，补齐后重跑即可。
已有不相关的同名目录或链接不会覆盖；不要用强制删除命令解决冲突。

完成后新开 Codex 对话，用 `$exec-deep-report` 调用；可在技能列表检查。
项目路径不可随意删除，因为安装使用指向该仓库的软链接。
更新已有安装：

```bash
git pull --ff-only
bash tools/install_codex.sh
```

独立安装单个技能目录时，若有 scripts/package.json，须在该技能自己的 scripts 目录
执行 npm install，再运行 doctor.py，不能只在平级 shared 目录装依赖。
安装检查不等于版式/内容审核，生成文档仍需看图和审阅论证。

## 安全回滚

升级前的公开备份：
[backup/pre-marketing-upgrade-20260925](https://github.com/raymondhuang1994/report-skills/tree/backup/pre-marketing-upgrade-20260925)，
与 v1.2.0 同提交 `41753293900c7da864e598a6e4aed0461afd197d`。
旧标签不覆盖、不改写历史；真实附件不在仓库。

仅在仓库没有未提交修改时，本机退回旧版：

```bash
git fetch origin --tags
git status --short
# 上一行应无输出；若有修改，先保存，不要强制切换
git switch --detach backup/pre-marketing-upgrade-20260925
```

现有 Codex 软链接仍指向同一目录，新对话读取旧版；旧版保留其原有已知问题，
不要用它的 render_qa 清理任何存放材料的目录。无需重跑旧版安装脚本。
回到新版：`git switch main`，再运行新版安装脚本。
本机切换不改变其他同事版本；团队默认分支需用新的 revert 提交回退，不 force-push。

## 其他宿主

- Claude.ai：从 [Releases](https://github.com/raymondhuang1994/report-skills/releases) 下载所需 .skill；
  按宿主技能上传入口导入。脚本功能需要具备代码执行环境及相关依赖。
- Claude Code：仓库保留原插件清单；入口为 `/plugin marketplace add raymondhuang1994/report-skills`，
  再 `/plugin install report-skills@report-skills`。本轮未实际运行 Claude Code 验证。
- 不支持技能目录的环境：Releases 的 prompts/*.md 可作方法参考；
  它不是一键可执行工具，生成 Word 和 QA 仍需要脚本环境。

## 验证与维护

```bash
python3 tools/sync_shared.py --check
bash tools/selftest.sh
python3 tools/package_skills.py --prompt-pack
```

- shared/ 是共用脚本与参考的唯一源；编辑后用 tools/sync_shared.py 同步。
- 自检在临时目录生成图、文档与 PDF，不改源码；错误退出码向上传递。
- qa.profile 为 short 可用于短材料；requiredModules 只声明所选模块。
- render_qa 输出父目录下的独立子目录，使用它打印的实际 PDF 路径。
- 行为回放走到最终选定材料，不只比章节或条数。测试说明见
  [evals/exec-deep-report.md](evals/exec-deep-report.md)，本轮结果见
  [docs/validation-v1.3.md](docs/validation-v1.3.md)。
- 发布前检查共享一致、测试、工作树变化和隐私，再打新版本标签。

## 隐私与使用边界

公开仓库只放方法、代码、虚构样例和不含敏感信息的测试摘要。
真实产品附件、客户资料、私有金标准和回放原文不上传；private/ 与 evals/gold/ 已忽略。
客户沟通产物是待审稿，不因 AI 打分或用户选择方向就变成合规批准稿。
