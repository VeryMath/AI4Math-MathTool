# MATLAB Runner

[English](README.md)

`matlab-runner` 是一个供各类 coding agent 使用的轻量 MATLAB
适配器。它不代替 MATLAB 或 MATLAB MCP Server，而是统一规定：什么时候
调用 MATLAB、怎样选择当前客户端实际提供的工具，以及怎样如实报告
执行、测试和数值验证结果。

当前是基于作者 `v0.1.8` 整理的 Review Candidate。本项目不是 MathWorks
官方产品，也不捆绑 MATLAB、MATLAB 许可证、MATLAB MCP Server 或 MATLAB
Agentic Toolkit。

## 作者

- 原作者：`njustar2002`
- GitHub 邮箱：`njustar2002@vip.163.com`

## 触发条件

只有用户明确要求使用 MATLAB、任务处理 `.m` 文件，或必须使用 MATLAB
工具箱、许可证、会话或真实运行结果时才调用。普通数学和通用编程
任务不会因为“MATLAB 也能做”而误触发。

## 执行流程

1. 只预检当前任务真正需要的环境能力。
2. 检查 coding agent 当前的工具目录。
3. 按 MATLAB MCP 能力和参数模式匹配实际工具。
4. 实现或检查 MATLAB 代码。
5. 需要执行时，通过已配置的 MATLAB MCP Server 真实运行。
6. 按需完成 MATLAB 单元测试和数值验证。
7. 统一报告调用、代码、文件、测试、验证标准和局限。

工具名不写死。coding agent 应该根据当前客户端实际暴露的名称调用
`evaluate_matlab_code` 等逻辑能力，无论客户端展示的是裸名、服务器前缀
还是命名空间。

## 配置

把这个 package 放到 coding agent 能加载 Skill 的位置，再按该客户端的
方式配置兼容的 MATLAB MCP Server。具体见
[`references/client-setup.md`](references/client-setup.md)。核心 Skill 不依赖固定安装路径。

## 验证

下列测试只验证 package 结构和跨客户端路由规则，不代表 MATLAB 已执行：

```bash
python3 -m unittest discover -s skills/matlab-runner/tests -v
```

作者与发布授权见 [`PROVENANCE.yaml`](PROVENANCE.yaml)，公开版整理记录见
[`NORMALIZATION.md`](NORMALIZATION.md)。
