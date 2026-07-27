# AI4Math-MathTool

AI4Math-MathTool 是 VeryMath 用于承载独立数学工具的仓库。进入本仓库的工具应具有
稳定的数据合同、可执行脚本和可独立验证的运行行为。

## 已纳入工具

| 工具 | 用途 | 状态 |
| --- | --- | --- |
| [`math-glossary`](skills/math-glossary/) | 构建、审阅、备份、导入、导出和维护双语数学术语库 | 本地课程版候选；贡献者授权与许可证确认前禁止公开发布 |

每个 package 独立保留自己的工作流、依赖、来源、规范化记录和测试。课程来源只作为
元数据，不作为代码仓库的职责边界。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
```

## 发布状态

当前 checkout 是尚未公开的审查候选。原始提交另存于教师控制、Git 忽略的档案目录。
在贡献者公开授权、署名偏好、仓库许可证和第三方材料审查全部确认前，不得创建公开
仓库或发布版本。

当前权利门槛见 [LICENSE_STATUS.md](LICENSE_STATUS.md)。
