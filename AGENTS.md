# AGENTS.md（给 Codex 及其他代理）

本仓库是一组“技能”：每个 `skills/<name>/SKILL.md` 描述一种任务的工作法，同目录下的 `references/`、`assets/`、`scripts/`、`examples/` 是它需要的文件。用户要写中文深度报告、口号、核查材料、销售问答或排版 Word 时，先读对应技能的 SKILL.md，按它的步骤做。

- 不知道用哪个：完整报告 → `exec-deep-report`；只要一块 → 对应卫星技能。
- 脚本运行前先 `python3 shared/scripts/doctor.py`；Node 依赖在 `shared/scripts` 下 `npm install`。
- 每个数字带来源与日期；材料内部口径矛盾单独列出；不写“唯一”“首只”“稳赚”一类慎用词（见 `shared/references/caution-words.md`）。
- 没有联网检索能力时，把需要检索的项写进数据缺口，不要用记忆里的数字冒充查证结果。
- 不能查看图片时，`render_qa.py` 生成的缩略图交给用户看，并在交付说明里写明“版式未经代理目视检查”。
- 只改任务需要的文件；共用文件改 `shared/` 再运行 `python3 tools/sync_shared.py`。
