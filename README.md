# report-skills：中文深度报告技能集

给管理层、董事会、产品委员会与销售团队写报告的工作法与工具链，打包成可安装的技能。一个编排器加四个卫星：

| 技能 | 用途 | 单独用的触发词 |
|---|---|---|
| `exec-deep-report` | 完整报告（产品分析与营销、机构或行业深度、新品候选池）。阶段 0 先确认生成内容、调用模块与输出形式，默认全选 | 做一份报告、深度分析、给老板或董事会看 |
| `product-slogan` | 定位句与口号，简繁英三版候选池、七维评分、熊市与撞车测试 | 想 slogan、口号、一句话 |
| `material-factcheck` | 核路演材料的数字：抽图表底层数据、逐只加总、复算集中度与费用、列矛盾 | 核一下材料、数字对不对 |
| `sales-qa-battlecard` | 问答、攻防表、适配矩阵、一分钟话术 | 客户会怎么问、攻防表、谁不适合买 |
| `cn-docx-report` | report.json 一次渲染成中文 Word，结构、文字、版式三道 QA | 排成 Word、版式检查 |

## 安装

**Claude.ai 网页或 App（含 Cowork）**：下载 Releases 里的 `<技能名>.skill`（或本地运行 `python3 tools/package_skills.py` 生成到 `dist/`），在 Customize → Skills 上传。Team 或 Enterprise 版可由上传者分享给指定同事或全组织。更新时重新上传同名文件。

**Claude Code**：仓库含 `.claude-plugin/marketplace.json`，在 Claude Code 里执行

```
/plugin marketplace add <GitHub 用户名>/report-skills
/plugin install report-skills@report-skills
```

仓库在个人账号下且为私有：先在 GitHub 的 Settings → Collaborators 把同事加为协作者，同事本机 `gh auth login` 或配好 SSH 后，终端里 `git clone` 能通就能装。更新：`/plugin marketplace update report-skills`。首次修改清单后请运行 `claude plugin validate .` 校验。

**Codex**：

```
git clone <仓库地址> && cd report-skills
tools/install_codex.sh          # 软链到 ~/.agents/skills
python3 shared/scripts/doctor.py && (cd shared/scripts && npm install)
```

Codex 里输入 `/skills` 查看，`$exec-deep-report` 可显式调用。更新：`git pull`。实测清单见 `docs/codex-smoke-test.md`。

**ChatGPT 或其他不支持技能目录的宿主**：用 `dist/prompts/<技能名>.md`（`python3 tools/package_skills.py --prompt-pack` 生成），整份粘贴进项目指令。脚本类功能（Word 渲染、QA、pptx 抽取）需要能执行代码的环境。

## 推送与发布（个人账号）

```
unzip report-skills-repo.zip && cd report-skills
git commit --amend --reset-author --no-edit          # 首次提交作者改成本机 git 身份
gh repo create report-skills --private --source=. --push   # 或先在网页新建私有仓库，再：
# git remote add origin git@github.com:<GitHub 用户名>/report-skills.git && git push -u origin main
git tag v1.2.0 && git push origin v1.2.0             # 触发 Actions：自检、打包、发布到 Releases
```

Releases 里的 `.skill` 与 `prompts/*.md` 供同事下载；私有仓库需登录 GitHub 才能下载。

## 使用顺序

1. 完整报告：直接对 `exec-deep-report` 提需求，它会先用选项确认范围与输出，再走两步交付（先执行摘要、事实底稿、骨架与缺口，确认后成稿）。
2. 只要一块：对应卫星技能直接出，不走立项问答。
3. 首次在本机使用先跑 `python3 shared/scripts/doctor.py`，缺什么按提示装。

## 维护规则

- `shared/` 是脚本与共用参考的唯一源。改那里，然后 `python3 tools/sync_shared.py`；提交前 `python3 tools/sync_shared.py --check` 必须通过。各技能的 `shared.txt` 是它同步的清单。
- 改规则前先跑 `tools/selftest.sh`；改完再跑一次。
- 每次改版：升 `VERSION` 与各技能 SKILL.md 里的版本号，写 `CHANGELOG.md`，用私有金标准回放一次（做法见 `skills/exec-deep-report/references/quality-rubric.md`），得分不低于上一版再打 tag。打 tag 后 GitHub Actions 自动自检、打包并发布到 Releases。
- 新踩的版式坑写进 `shared/references/docx-pitfalls.md`；新表格模板写进 `shared/references/toolkit-templates.md`；`structure_qa.py` 抓不到的新规则加进去。

## 隐私与合规

- 仓库只放方法、脚本与虚构样例；不放任何真实材料、金标准终稿、回放记录（已在 `.gitignore` 排除 `private/`、`evals/gold/`）。
- 技能产出一律标“内部讨论稿，未经合规审阅”；慎用词表在 `shared/references/caution-words.md`，监管细则由各自的项目知识库提供。
- 是否可以放在 GitHub、放公司组织号还是个人号，以本公司 IT 与合规政策为准。

## 目录

```
skills/            五个技能，每个自带所需文件（宿主之间不能互相引用路径）
shared/            唯一源：scripts/、references/、examples/
tools/             sync_shared.py、package_skills.py、selftest.sh、install_codex.sh
evals/             每个技能的验收题（只用公开材料）
docs/              Codex 实测清单等
.claude-plugin/    Claude Code 插件与 marketplace 清单
.github/workflows/ 打 tag 自动发布
```
