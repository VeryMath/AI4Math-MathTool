# math-glossary

`math-glossary` 用于构建和维护双语数学术语库，并以 JSON 文件作为唯一事实源。它
提供备份、Excel 导入导出、可选的 AI 例句补全和可选的本地 Flask 管理界面。

课程版将学生提交作为一个独立 Skill 保留，不合并、不继承其他 VeryMath Skill。此次
整理只处理目录、可移植性、安全、显式配置、文档和测试，不改变原始工具的核心用途与
工作流。

## 能力

- 从 PDF、文本、Markdown、Excel、JSON、CSV、YAML、MDX 和 OCR 结果中提取或
  引导整理术语；
- 从 CSV/TSV/JSON/YAML 直接构建 `glossary.json`，并记录来源文件位置；
- 按 [`references/glossary-schema.md`](references/glossary-schema.md) 与
  [`references/glossary.schema.json`](references/glossary.schema.json) 排序、编号、
  合并和维护术语；
- 备份 `glossary.json`，并与 Excel 双向转换；
- 运行本地 Web 搜索与增删改查界面；
- 通过用户显式配置的 OpenAI-compatible endpoint，可选补全缺失例句。

## 安装

离线核心工具：

```bash
python3 -m pip install -r requirements.txt
```

可选 AI 例句补全：

```bash
python3 -m pip install -r requirements-ai.txt
```

安装依赖前应先向用户说明并获得确认。`mdict-utils` 仅在解包 MDX 时需要。
Web 界面没有身份认证，应保持默认的 loopback 绑定，不要暴露到不可信网络。

## 最小验证

```bash
python3 -m unittest discover -s tests -v
```

从结构化数据建库：

```bash
python3 scripts/glossary_build.py /path/to/terms.csv
```

默认输出 `/path/to/术语库/glossary.json`。除非显式添加 `--force`，否则不会覆盖
已有 JSON。缺少 Excel 依赖时，命令会明确报告“JSON 完成、Excel 待完成”，并以
状态码 3 退出。

导出已有术语库：

```bash
python3 scripts/glossary_export.py export /path/to/glossary.json /path/to/output
```

启动本地 Web 界面且不自动打开浏览器：

```bash
python3 scripts/glossary_web.py \
  --glossary /path/to/glossary.json \
  --no-browser
```

完整工作流和整理边界见 [`SKILL.md`](SKILL.md) 与
[`NORMALIZATION.md`](NORMALIZATION.md)。

## 发布状态

当前版本是采用 MIT 许可、可以进入远端发布流程的本地发布候选。公开指令、课程版
整理批准和第三方材料审查已记录在 [`PROVENANCE.yaml`](PROVENANCE.yaml)。
在公开仓库、通过的 CI 运行与 release tag 实际存在前，不把它描述为已公开发布。
贡献者公开姓名按课程统一规则标为 **Yunfeng Lu**。
