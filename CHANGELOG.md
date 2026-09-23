# 仓库变更记录

## 1.2.0（2026-09-22）
- 首个多技能版本：exec-deep-report 1.2（编排器）；product-slogan、material-factcheck、sales-qa-battlecard、cn-docx-report 各 0.1。
- `shared/` 为脚本与参考的唯一源，`tools/sync_shared.py --check` 保证一致。
- `tools/package_skills.py` 产出各技能的 .skill（Claude.ai 上传用）与单文件提示包（ChatGPT 项目用）。
- Claude Code 插件与 marketplace 清单；Codex 元数据与安装脚本；GitHub Actions 打 tag 自动发布。
- 各技能内的变更见 `skills/exec-deep-report/CHANGELOG.md`。
