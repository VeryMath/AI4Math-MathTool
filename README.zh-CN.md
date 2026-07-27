# AI4Math-MathTool

AI4Math-MathTool 是 VeryMath 用于承载独立数学工具的仓库。进入本仓库的工具应具有
稳定的数据合同、可执行脚本和可独立验证的运行行为。

## 已纳入工具

| 工具 | 用途 | 状态 |
| --- | --- | --- |
| [`math-glossary`](skills/math-glossary/) | 构建、审阅、备份、导入、导出和维护双语数学术语库 | 已按 MIT 许可发布 [`v0.1.0`](https://github.com/VeryMath/AI4Math-MathTool/releases/tag/v0.1.0) |

每个 package 独立保留自己的工作流、依赖、来源、规范化记录和测试。课程来源只作为
元数据，不作为代码仓库的职责边界。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
```

## 发布状态

当前仓库是公开的 canonical repository，首个
[`v0.1.0`](https://github.com/VeryMath/AI4Math-MathTool/releases/tag/v0.1.0)
版本采用 [MIT License](LICENSE)。源码公开指令与第三方材料审查结果记录在
[`skills/math-glossary/PROVENANCE.yaml`](skills/math-glossary/PROVENANCE.yaml)。
原始提交仍单独保存在教师控制、Git 忽略的档案目录；贡献者姓名统一按课程名册转写为
英文 `Given-name Surname`。

依赖与材料边界见 [THIRD_PARTY.md](THIRD_PARTY.md)，安全说明见
[SECURITY.md](SECURITY.md)，创建远端、运行 CI 与发布版本的步骤见
[PUBLISHING.md](PUBLISHING.md)。
