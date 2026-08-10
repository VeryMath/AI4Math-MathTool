---
name: ai4math-math-tool
description: "Route requests to standalone AI4Math mathematical tools. Use when a user asks to build or maintain a bilingual mathematical glossary, manage mathematical terminology, or select an available MathTool package."
---

# AI4Math MathTool Router

Route each request to the narrowest matching package:

| Request | Package |
| --- | --- |
| Build, update, query, back up, import, export, or review a bilingual mathematical glossary | `skills/math-glossary/SKILL.md` |
| Explicitly use MATLAB, operate on `.m` files, or obtain MATLAB-specific execution, test, toolbox, license, or numerical-validation evidence | `skills/matlab-runner/SKILL.md` |

Before running a package:

1. Read its `SKILL.md`.
2. Check its declared dependencies without installing them automatically.
3. Keep all user data and generated files in an explicit user-selected working
   directory.
4. Report missing dependencies, destructive operations, and publication
   constraints before acting.
