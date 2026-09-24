# 仓库变更记录

## 1.3.0（2026-09-25）
- 方向确认前移：推荐完整分析/部分模块/现稿优化，先给叙事小样与取舍，用户确认后再执行；已有明确授权不重复问。
- 创意按需展开：先方向后句子；研究/传播/双层表达；原句 exact/spirit/reference 保留，候选与已选状态分开。
- 新增主张卡：事实/计算到机制、产品承接、替代、反证、客户价值；同底稿按需生成研究、培训、客户待审稿。
- 修正样例的绝对权重/相对权重混用、资本开支与 AUM 的无效推论和日期口径；语义验收取代篇幅与“惊人”数量门槛。
- 安装与 QA：依赖按真实执行路径安装、安全独立渲染目录、错误传播、短材料及显式模块检查、自检不修改源码。
- 回滚基线：GitHub 标签 backup/pre-marketing-upgrade-20260925（与 v1.2.0 同提交）；不重写历史。
- 行为回放使用虚构材料；没有把真实附件或私有金标准上传。测试结论与未验证项见 docs/validation-v1.3.md。

## 1.2.0（2026-09-22）
- 首个多技能版本：exec-deep-report 1.2（编排器）；product-slogan、material-factcheck、sales-qa-battlecard、cn-docx-report 各 0.1。
- `shared/` 为脚本与参考的唯一源，`tools/sync_shared.py --check` 保证一致。
- `tools/package_skills.py` 产出各技能的 .skill（Claude.ai 上传用）与单文件提示包（ChatGPT 项目用）。
- Claude Code 插件与 marketplace 清单；Codex 元数据与安装脚本；GitHub Actions 打 tag 自动发布。
- 各技能内的变更见 `skills/exec-deep-report/CHANGELOG.md`。
