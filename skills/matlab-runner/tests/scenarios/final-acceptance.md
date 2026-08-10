# v0.1.8 最终验收提示词

这些提示词用于验证 v0.1.8 的最终恢复和调用预算规则。它们不会被
Python 结构测试自动执行；本公开 package 也不把历史审阅摘要当作当前
MATLAB 运行证据。要宣称验收通过，必须在真实 MATLAB 环境中单独运行并保留结果。

## 测试 1：硬性一次调用上限

```text
请原样使用 MATLAB 执行 A = [1 2; 3];。

要求：
1. 第一个工具调用前加载 matlab-runner；
2. 最多只允许一次 MATLAB MCP 调用；
3. 不得修复代码，不得重试；
4. 返回 MATLAB 真实错误；
5. 完成状态为 failed；
6. 错误类型为 MATLAB_EXECUTION_ERROR；
7. 摘要写 MATLAB tool calls: total 1，并说明调用上限已满足。
```

理想行为：一次调用失败后停止，不擅自进行第二次调用。

## 测试 2：ODE 单次完整验证

```text
请实际使用 MATLAB 求解 y'=-2y+sin(t)，y(0)=1，0≤t≤5，
比较 ode45 默认设置和 RelTol=1e-9、AbsTol=1e-12。

要求：
1. 加载 matlab-runner；
2. 只读取 numerical-safety reference；
3. 最多一次 MATLAB MCP 调用；
4. 使用正确解析解 y=(6/5)e^(-2t)+(2/5)sin(t)-(1/5)cos(t)；
5. 显式定义解析导数 yPrime；
6. 用 yPrime(t)+2*yExact(t)-sin(t) 验证残差；
7. tq、数值解与解析解全部为 51×1；
8. 相减前 assert 尺寸一致；
9. 输出候选初值、正确解初值、最大残差和两组最大绝对误差；
10. 不查询默认容差值，不追加诊断；
11. 摘要写 MATLAB tool calls: total 1，且未生成文件。
```

作者提供的预期误差接近下列数值，实际验收应以当次 MATLAB 输出为准：

```text
默认设置：2.854e-04
严格设置：8.824e-11
```

## 测试 3：软性一次调用目标与超时

```text
请判断当前 MATLAB 环境是否可以使用 Optimization Toolbox 的 fmincon。

尽量在一次针对性调用中完成，但这不是硬性上限。分别检查：
- ver('optim')
- which/exist('fmincon')
- license('test','Optimization_Toolbox')

若调用超时，可以进行一次最小化恢复。必须：
1. 把超时记录为 MCP_TOOL_TIMEOUT；
2. 最终写 success (after recovery)；
3. 报告真实总调用数；
4. 说明“一次调用”的软目标是否满足；
5. 不猜测安装根因。
```
