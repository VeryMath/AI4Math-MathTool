# AI4Math-MathTool

[English](README.md)

AI4Math-MathTool 是 VeryMath 用于承载独立数学工具和轻量 coding-agent
适配器的仓库。每个 package 都提供明确的工作流、来源记录和可独立验证的行为。

## 已纳入工具

| 工具 | 用途 | 状态 |
| --- | --- | --- |
| [`math-glossary`](skills/math-glossary/) | 构建、审阅、备份、导入、导出和维护双语数学术语库 | 已按 MIT 许可发布 [`v0.1.0`](https://github.com/VeryMath/AI4Math-MathTool/releases/tag/v0.1.0) |
| [`matlab-runner`](skills/matlab-runner/) | 把明确的 MATLAB 任务路由到已配置的 MATLAB MCP Server，并记录执行、测试和数值验证证据 | Review Candidate，尚未发布 Release |

每个 package 独立保留自己的工作流、依赖、来源、规范化记录和测试。课程来源只作为
元数据，不作为代码仓库的职责边界。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
python3 -m unittest discover -s skills/matlab-runner/tests -v
```

## 发布状态

当前仓库是公开的 canonical repository，首个
[`v0.1.0`](https://github.com/VeryMath/AI4Math-MathTool/releases/tag/v0.1.0)
版本采用 [MIT License](LICENSE)。源码公开指令与第三方材料审查结果记录在
[`skills/math-glossary/PROVENANCE.yaml`](skills/math-glossary/PROVENANCE.yaml)。
原始提交仍单独保存在教师控制、Git 忽略的档案目录；贡献者姓名统一按课程名册转写为
英文 `Given-name Surname`。

`matlab-runner` 是由 `njustar2002` 贡献的独立 Review Candidate，发布授权与
原始文件校验值记录在
[`skills/matlab-runner/PROVENANCE.yaml`](skills/matlab-runner/PROVENANCE.yaml)。
它不属于历史 `v0.1.0` Release。

依赖与材料边界见 [THIRD_PARTY.md](THIRD_PARTY.md)，安全说明见
[SECURITY.md](SECURITY.md)，创建远端、运行 CI 与发布版本的步骤见
[PUBLISHING.md](PUBLISHING.md)。
